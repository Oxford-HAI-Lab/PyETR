def main():
    with open("./pyetr/cases.py", "r") as f:
        cases_file = f.readlines()

    import pyetr.cases
    from pyetr.cases import BaseExample

    out = []
    for name, case in vars(pyetr.cases).items():
        if (
            isinstance(case, type)
            and issubclass(case, BaseExample)
            and case != BaseExample
        ):
            out.append(name)
    end_num: int = 0
    for i, line in enumerate(cases_file):
        if line[0] == "]":
            end_num = i + 1
            break
    new_lines = ["__all__ = [\n"]
    for item in out:
        new_lines.append(f'    "{item}",\n')
    new_lines.append("]\n")
    new_lines += cases_file[end_num:]

    with open("./pyetr/cases.py", "w") as f:
        cases_file = f.writelines(new_lines)
