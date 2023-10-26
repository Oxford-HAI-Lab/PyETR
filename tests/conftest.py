import json
import re
from pathlib import Path

import pytest

import pyetr.cases
from pyetr import ArbitraryObject, Function, FunctionalTerm
from pyetr.cases import BaseExample
from pyetr.parsing.fol_parser.unparse_view import FOLNotSupportedError
from pyetr.parsing.view_parser import ViewParser


class ExampleCollector(pytest.File):
    def collect(self):
        classes: list[ExampleItem] = []
        assert self.parent is not None
        for name, case in vars(pyetr.cases).items():
            if (
                isinstance(case, type)
                and issubclass(case, BaseExample)
                and case != BaseExample
            ):
                classes.append(
                    ExampleItem.from_parent(parent=self, test_class=case, name=name)
                )
        return classes


class ExampleItem(pytest.Item):
    def __init__(self, *args, test_class: type[BaseExample], **kwargs):
        super().__init__(*args, **kwargs)
        self.test_class = test_class

    def runtest(self):
        self.test_class.test()

    def reportinfo(self):
        return self.fspath, None, f"custom test: {self.test_class.__name__}"


def replace_emphasis(input_string):
    return re.sub(
        r"(\w+\*|\([^()]*\))",
        lambda match: match.group(1).replace("*", ""),
        input_string,
    )


def length_identity_test(start: str, end: str) -> bool:
    start = start.replace(" ", "")
    end = end.replace(" ", "")
    # First replace sums
    start = start.replace("++", "σ")
    end = end.replace("++", "σ")
    # Then replace forall etc
    start = start.replace("∃", "E")
    start = start.replace("∀", "A")
    end = end.replace("∃", "E")
    end = end.replace("∀", "A")
    if len(start) == len(end) and sorted(start, key=hash) == sorted(end, key=hash):
        return True

    # Then remove emphasis
    start = replace_emphasis(start)
    end = replace_emphasis(end)

    if len(start) == len(end) and sorted(start, key=hash) == sorted(end, key=hash):
        return True
    return False


parse_test_exemptions = [
    "{0.85**0.1=* E(j()*)D(j())H(j()), 0.85**0.9=* E(j())D(j())~H(j()), 0.15**0.1=* E(j())~D(j())H(j()), 0.15**0.9=* E(j())~D(j())~H(j())}"
]


class BaseParseItem(pytest.Item):
    def __init__(self, *args, view_string: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_string = view_string

    def reportinfo(self):
        return self.fspath, None, f"ViewString: {self.view_string}"


class ParseTestItem(BaseParseItem):
    def runtest(self):
        vp = ViewParser()
        parsed_view = vp.from_str(self.view_string)
        string_recovered = vp.to_str(parsed_view, round_ints=False)
        alt_string = vp.to_str(parsed_view, round_ints=True)
        if (
            not length_identity_test(self.view_string, string_recovered)
            and not length_identity_test(self.view_string, alt_string)
            and self.view_string not in parse_test_exemptions
        ):
            raise ValueError(
                f"String recovered: {string_recovered} or alt {alt_string}, compared to {self.view_string}"
            )


class ParseCompareViaJson(BaseParseItem):
    def runtest(self):
        vp = ViewParser()
        parsed_view = vp.from_str(self.view_string)
        out_view = vp.from_json(vp.to_json(parsed_view))
        if parsed_view != out_view:
            raise ValueError(
                f"View lost in json conversion, start: {parsed_view}, end: {out_view}"
            )
        out_view = vp.from_json(vp.to_json(parsed_view))
        if parsed_view != out_view:
            raise ValueError(
                f"View lost in yoyo json conversion, start: {parsed_view}, end: {out_view}"
            )


class ParseCompareViaString(BaseParseItem):
    def runtest(self):
        vp = ViewParser()
        parsed_view = vp.from_str(self.view_string)
        out_view = vp.from_str(vp.to_str(parsed_view))
        if parsed_view != out_view:
            raise ValueError(
                f"View lost in yoyo string conversion, start: {parsed_view}, end: {out_view}"
            )


class ParseCompareViaFOL(BaseParseItem):
    def runtest(self):
        vp = ViewParser()
        parsed_view = vp.from_str(self.view_string)

        try:
            out_view = vp.from_fol(vp.to_fol(parsed_view))
            if parsed_view != out_view:
                raise ValueError(
                    f"View lost in yoyo FOL conversion, start: {parsed_view}, end: {out_view}"
                )
        except FOLNotSupportedError:
            pass


parse_test_set: list[type[BaseParseItem]] = [
    ParseTestItem,
    ParseCompareViaJson,
    ParseCompareViaString,
    ParseCompareViaFOL,
]


class ParseTestCollector(pytest.File):
    def collect(self):
        with open(self.path) as f:
            json_file: list[str] = json.load(f)
        for test_set in parse_test_set:
            for item in json_file:
                yield test_set.from_parent(parent=self, view_string=item, name=item)


def is_case_file(path: Path) -> bool:
    return re.match(re.compile(r"test_cases.py"), path.name) is not None


def is_case_list(path: Path) -> bool:
    return (
        re.match(re.compile(r"case_list.json"), path.name) is not None
        or re.match(re.compile(r"case_list_extra.json"), path.name) is not None
    )


def pytest_collect_file(parent: pytest.Session, file_path: Path):
    if is_case_file(file_path):
        return ExampleCollector.from_parent(parent=parent, path=file_path)
    elif is_case_list(file_path):
        return ParseTestCollector.from_parent(parent=parent, path=file_path)


@pytest.fixture
def func():
    return Function("func", 1)


@pytest.fixture
def arb_obj():
    return ArbitraryObject("x1")


@pytest.fixture
def term(func, arb_obj):
    return FunctionalTerm(func, (arb_obj,))
