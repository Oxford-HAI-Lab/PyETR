with open("../pyetr/cases.py", "r") as f:
    out = f.readlines()

import json
import re

from pyetr.cases import BaseExample
from pyetr.new_parsing import parse_view_to_string as parse_new_view_to_string
from pyetr.parsing import parse_string_to_view
from pyetr.view import View

pattern = r'"(.*?)"'


output_dict: dict[str, str] = {}
for line in out:
    matches = re.findall(pattern, line)
    for match in matches:
        try:
            new_view = parse_string_to_view(match)
        except:
            new_view = None
        if new_view is not None:
            output_dict[match] = parse_new_view_to_string(new_view)

print(output_dict)

json.dump(output_dict, open("out.json", "w+"), indent=2)
