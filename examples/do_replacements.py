import json
from copy import copy

with open("../pyetr/cases.py", "r") as f:
    out = f.readlines()

replacements: dict[str, str] = json.load(open("out.json"))

print(out)
print(replacements)

with open("../pyetr/cases.py", "w") as f:
    for line in out:
        new_line = copy(line)
        for key in sorted(replacements, key=lambda x: len(x), reverse=True):
            print(f"{key}: {replacements[key]}")
            old_phrase = f'"{key}"'
            new_phrase = f'"{replacements[key]}"'
            new_line = new_line.replace(old_phrase, new_phrase)
        f.write(new_line)
