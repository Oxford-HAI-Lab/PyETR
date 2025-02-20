import json
import re
from pathlib import Path
from typing import Any

import pytest

import pyetr.cases
from pyetr import ArbitraryObject, Function, FunctionalTerm
from pyetr.cases import BaseExample
from pyetr.exceptions import OperationUndefinedError
from pyetr.issues import IssueStructure
from pyetr.parsing.common import ParsingError
from pyetr.parsing.fol_items.view_to_items import FOLNotSupportedError
from pyetr.view import View


class ExampleCollector(pytest.File):
    def collect(self):
        classes: list[ExampleItem] = []
        assert self.parent is not None
        for name in pyetr.cases.__all__:
            case = getattr(pyetr.cases, name)
            classes.append(
                ExampleItem.from_parent(parent=self, test_class=case, name=name)
            )
        return classes


class ExampleItem(pytest.Item):
    def __init__(self, *args: Any, test_class: type[BaseExample], **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.test_class = test_class

    def runtest(self):
        self.test_class.test(verbose=True)

    def reportinfo(self):
        return self.fspath, None, f"custom test: {self.test_class.__name__}"


def replace_emphasis(input_string):
    return re.sub(
        r"(\w+\*|\([^()]*\))",
        lambda match: match.group(1).replace("*", ""),
        input_string,
    )


def replace_letters(s: str) -> str:
    return s.replace(" ", "").replace("++", "σ").replace("∃", "E").replace("∀", "A")


def length_identity_test(start: str, end: str) -> bool:
    start = replace_letters(start)
    end = replace_letters(end)
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
        parsed_view = View.from_str(self.view_string)
        assert parsed_view.detailed
        string_recovered = parsed_view.to_str(round_ints=False)
        alt_string = parsed_view.to_str(round_ints=True)
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
        parsed_view = View.from_str(self.view_string)
        out_view = View.from_json(parsed_view.to_json())
        if parsed_view != out_view:
            raise ValueError(
                f"View lost in json conversion, start: {parsed_view}, end: {out_view}"
            )
        out_view = View.from_json(parsed_view.to_json())
        if parsed_view != out_view:
            raise ValueError(
                f"View lost in yoyo json conversion, start: {parsed_view}, end: {out_view}"
            )


class ParseCompareViaString(BaseParseItem):
    def runtest(self):
        parsed_view = View.from_str(self.view_string)
        out_view = View.from_str(parsed_view.to_str())
        if parsed_view != out_view:
            raise ValueError(
                f"View lost in yoyo string conversion, start: {parsed_view}, end: {out_view}"
            )


class ParseCompareViaFOL(BaseParseItem):
    def runtest(self):
        parsed_view = View.from_str(self.view_string)

        try:
            out_view = View.from_fol(parsed_view.to_fol())
            if parsed_view != out_view:
                raise ValueError(
                    f"View lost in yoyo FOL conversion, start: {parsed_view}, end: {out_view}"
                )
        except FOLNotSupportedError:
            pass


class ParseCompareViaSMT(BaseParseItem):
    def runtest(self):
        parsed_view = View.from_str(self.view_string)

        try:
            out_view = View.from_smt(parsed_view.to_smt())
            compare_view = View.with_defaults(
                stage=parsed_view.stage,
                supposition=parsed_view.supposition,
                dependency_relation=parsed_view.dependency_relation,
                issue_structure=IssueStructure(),
                weights=parsed_view.weights,
            )
            if compare_view != out_view:
                raise ValueError(
                    f"View lost in yoyo SMT conversion, start: {compare_view}, end: {out_view}"
                )
        except FOLNotSupportedError:
            pass


class ParseCompareViaSMTLib(BaseParseItem):
    def runtest(self):
        parsed_view = View.from_str(self.view_string)

        try:
            out_view = View.from_smt_lib(parsed_view.to_smt_lib())
            compare_view = View.with_defaults(
                stage=parsed_view.stage,
                supposition=parsed_view.supposition,
                dependency_relation=parsed_view.dependency_relation,
                issue_structure=IssueStructure(),
                weights=parsed_view.weights,
            )
            if compare_view != out_view:
                raise ValueError(
                    f"View lost in yoyo SMT Lib conversion, start: {compare_view}, end: {out_view}"
                )
        except FOLNotSupportedError:
            pass


class ParseFailure(BaseParseItem):
    def runtest(self):
        with pytest.raises(ParsingError):
            View.from_str(self.view_string)


class OperationTest(pytest.Item):
    def __init__(
        self,
        *args,
        view_string1: str,
        view_string2: str,
        view1: View,
        view2: View,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.view_string1 = view_string1
        self.view_string2 = view_string2
        self.view1 = view1
        self.view2 = view2

    def reportinfo(self):
        return (
            self.fspath,
            None,
            f"ViewString1: {self.view_string1}, ViewString2: {self.view_string2}",
        )

    def runtest(self):
        parsed_view1 = self.view1
        parsed_view2 = self.view2

        parsed_view1.product(parsed_view2)
        try:
            parsed_view1.sum(parsed_view2)
        except OperationUndefinedError:
            pass
        parsed_view1.atomic_answer(parsed_view2)
        parsed_view1.equilibrium_answer(parsed_view2)
        parsed_view1.answer(parsed_view2)
        parsed_view1.merge(parsed_view2)
        parsed_view1.update(parsed_view2)
        parsed_view1.universal_product(parsed_view2)
        parsed_view1.existential_sum(parsed_view2)
        parsed_view1.factor(parsed_view2)
        parsed_view1.inquire(parsed_view2)
        parsed_view1.suppose(parsed_view2)
        parsed_view1.query(parsed_view2)
        parsed_view1.which(parsed_view2)


parse_test_set: list[type[BaseParseItem]] = [
    ParseTestItem,
    ParseCompareViaJson,
    ParseCompareViaString,
    ParseCompareViaFOL,
    ParseCompareViaSMT,
    ParseCompareViaSMTLib,
]


class ParseTestCollector(pytest.File):
    def collect(self):
        with open(self.path) as f:
            json_file: list[str] = json.load(f)
        for test_set in parse_test_set:
            for item in json_file:
                yield test_set.from_parent(parent=self, view_string=item, name=item)
        if self.config.option.viewops:
            parsed_json = [(i, View.from_str(i)) for i in json_file]
            for item1, parsed_view1 in parsed_json:
                for item2, parsed_view2 in parsed_json:
                    if item1 != item2:
                        yield OperationTest.from_parent(
                            parent=self,
                            view_string1=item1,
                            view_string2=item2,
                            view1=parsed_view1,
                            view2=parsed_view2,
                            name="View1:" + item1 + " View2:" + item2,
                        )


class ParseFailureCollector(pytest.File):
    def collect(self):
        with open(self.path) as f:
            json_file: list[str] = json.load(f)
        for item in json_file:
            yield ParseFailure.from_parent(parent=self, view_string=item, name=item)


def is_case_file(path: Path) -> bool:
    return re.match(re.compile(r"test_cases.py"), path.name) is not None


def is_case_list(path: Path) -> bool:
    return re.match(re.compile(r"case_list.json"), path.name) is not None


def is_failure_file(path: Path) -> bool:
    return re.match(re.compile(r"failure_list.json"), path.name) is not None


def pytest_collect_file(parent: pytest.Session, file_path: Path):
    if is_case_file(file_path):
        return ExampleCollector.from_parent(parent=parent, path=file_path)
    elif is_case_list(file_path):
        return ParseTestCollector.from_parent(parent=parent, path=file_path)
    elif is_failure_file(file_path):
        return ParseFailureCollector.from_parent(parent=parent, path=file_path)


@pytest.fixture
def func():
    return Function("func", 1)


@pytest.fixture
def arb_obj():
    return ArbitraryObject("x1")


@pytest.fixture
def term(func: Function, arb_obj: ArbitraryObject):
    return FunctionalTerm(func, (arb_obj,))


def pytest_addoption(parser):
    parser.addoption(
        "--viewops",
        dest="viewops",
        action="store_true",
        help="Include view op tests?",
    )
