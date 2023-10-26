import json
import re
from pathlib import Path

import pytest

import pyetr.cases
from pyetr import ArbitraryObject, Function, FunctionalTerm
from pyetr.cases import BaseExample
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


def remove_dot_zero(input_string):
    # Define a regular expression pattern to match ".0" but not ".00"
    pattern = r"\.0(?!0)"

    # Use re.sub() to replace ".0" with nothing
    result_string = re.sub(pattern, "", input_string)

    return result_string


def length_identity_test(start: str, end: str) -> bool:
    start = start.replace(" ", "")
    end = end.replace(" ", "")
    # First replace sums
    start = start.replace("++", "σ")
    end = end.replace("++", "σ")
    if len(start) == len(end):
        return True

    # Then remove emphasis
    start = replace_emphasis(start)
    end = replace_emphasis(end)

    if len(start) == len(end):
        return True

    return False


parse_test_exemptions = [
    "{0.85**0.1=* E(j()*)D(j())H(j()), 0.85**0.9=* E(j())D(j())~H(j()), 0.15**0.1=* E(j())~D(j())H(j()), 0.15**0.9=* E(j())~D(j())~H(j())}"
]


class ParseTestItem(pytest.Item):
    def __init__(self, *args, view_string: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.view_string = view_string

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

    def reportinfo(self):
        return self.fspath, None, f"ViewString: {self.view_string}"


class ParseTestCollector(pytest.File):
    def collect(self):
        with open(self.path) as f:
            json_file: list[str] = json.load(f)
        for item in json_file:
            yield ParseTestItem.from_parent(parent=self, view_string=item, name=item)


def is_case_file(path: Path) -> bool:
    return re.match(re.compile(r"test_cases.py"), path.name) is not None


def is_case_list(path: Path) -> bool:
    return re.match(re.compile(r"case_list.json"), path.name) is not None


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
