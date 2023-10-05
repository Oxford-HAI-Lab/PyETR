import json
from abc import ABCMeta
from collections import defaultdict

import pyetr.cases
from pyetr.cases import BaseExample
from pyetr.parsing import parse_view_to_string
from pyetr.view import View

case_vars = vars(pyetr.cases)


output_dict: dict[str, dict[str, str | tuple[str, ...]]] = defaultdict(dict)
for k, v in case_vars.items():
    if (
        v != ABCMeta
        and hasattr(v, "mro")
        and BaseExample in v.mro()
        and v != BaseExample
    ):
        assert issubclass(v, BaseExample)
        for attr, item in v.__dict__.items():
            if attr[0] != "_" and attr != "test":
                if not (isinstance(item, View) or isinstance(item, tuple)):
                    raise ValueError(f"{item}")
                elif isinstance(item, View):
                    output_dict[k][attr] = parse_view_to_string(item)
                else:
                    output_dict[k][attr] = tuple(
                        [parse_view_to_string(i) for i in item]
                    )
print(output_dict)

json.dump(output_dict, open("out.json", "w+"), indent=2)
