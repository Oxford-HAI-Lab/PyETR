import re
from pathlib import Path

import pytest

import pyetr.cases
from pyetr import ArbitraryObject, Function
from pyetr.cases import BaseExample
from pyetr.term import FunctionalTerm


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
                    ExampleItem.from_parent(
                        parent=self.parent, test_class=case, name=name
                    )
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


FILE_NAME_PATTERN = re.compile(r"test_cases.py")


def is_case_file(path: Path) -> bool:
    return re.match(FILE_NAME_PATTERN, path.name) is not None


def pytest_collect_file(parent: pytest.Session, file_path: Path):
    if is_case_file(file_path):
        return ExampleCollector.from_parent(parent, path=file_path)  # type:ignore


@pytest.fixture
def func():
    return Function("func", 1)


@pytest.fixture
def arb_obj():
    return ArbitraryObject("x1")


@pytest.fixture
def term(func, arb_obj):
    return FunctionalTerm(func, (arb_obj,))
