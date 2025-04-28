import inspect
from typing import Any, Optional


def get_line_no(item: Optional[Any], file_suffix: str):
    if item:
        # Get the source file and line number
        _, start_line_number = inspect.getsourcelines(item)
        url_prefix = f"https://github.com/Oxford-HAI-Lab/PyETR/blob/master/pyetr/{file_suffix}.py#L"
        return f"\n[Link to code]({url_prefix}{start_line_number})\n\n"
    else:
        return ""
