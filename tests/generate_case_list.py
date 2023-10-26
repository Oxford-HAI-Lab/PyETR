with open("../pyetr/cases.py", "r") as f:
    out = f.readlines()

import json
import re

from pyetr.parsing.common import ParsingError
from pyetr.parsing.view_parser import ViewParser

pattern = r'"(.*?)"'

vp = ViewParser()
output_list: list[str] = []
for line in out:
    matches = re.findall(pattern, line)
    for match in matches:
        try:
            new_view = vp.from_str(match)
        except ParsingError:
            new_view = None
        if new_view is not None and match not in output_list:
            output_list.append(match)

json.dump(output_list, open("case_list.json", "w+"), indent=2)
