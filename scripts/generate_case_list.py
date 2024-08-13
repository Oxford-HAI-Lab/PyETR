with open("./pyetr/cases.py", "r") as f:
    out = f.readlines()

import json
import re

from pyetr import View
from pyetr.parsing.common import ParsingError


def main():
    pattern = r'"(.*?)"'

    output_list: list[str] = []
    for line in out:
        matches = re.findall(pattern, line)
        for match in matches:
            try:
                new_view = View.from_str(match)
            except ParsingError:
                new_view = None
            if new_view is not None and match not in output_list:
                output_list.append(match)

    extras: list[str] = json.load(open("./tests/case_list_extra.json"))
    output_list += extras

    json.dump(output_list, open("./tests/case_list.json", "w+"), indent=2)
