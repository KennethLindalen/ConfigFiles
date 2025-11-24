import re
import os
import sys
from pathlib import Path

input_path = Path("C:/Users/KennethLindalen/Documents/Development/3. Private/SPSolver/classes.txt")
output_dir = Path("C:/Users/KennethLindalen/Documents/Development/3. Private/SPSolver/output_classes/")
output_dir.mkdir(parents=True, exist_ok=True)
text = input_path.read_text(encoding="utf-8")
class_pattern = re.compile(r"""((?:public|internal|protected|private|sealed|abstract|static|partial|new|readonly)\s+)*class\s+(?P<name>\w+)[^{]*{""",re.VERBOSE)

matches = list(class_pattern.finditer(text))

if not matches:
    print("No classes found in input file.")
    sys.exit(0)

print(f"Found {len(matches)} class declarations.")

def find_matching_brace(s: str, start_index: int) -> int:
    depth = 0
    i = start_index
    length = len(s)

    while i < length:
        ch = s[i]

        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return i
        i += 1

    raise ValueError(f"No matching closing brace for brace at position {start_index}")
name_counts = {}

for m in matches:
    class_name = m.group("name")
    class_start = m.start()
    open_brace_index = text.find('{', m.start())

    if open_brace_index == -1:
        print(f"Skipping {class_name}: could not find opening brace.")
        continue

    try:
        close_brace_index = find_matching_brace(text, open_brace_index)
    except ValueError as e:
        print(f"Skipping {class_name}: {e}")
        continue
    class_code = text[class_start:close_brace_index + 1].strip() + "\n"

    count = name_counts.get(class_name, 0)
    name_counts[class_name] = count + 1

    if count == 0:
        file_name = f"{class_name}.cs"
    else:
        file_name = f"{class_name}_{count}.cs"

    out_path = output_dir / file_name
    out_path.write_text(class_code, encoding="utf-8")
    print(f"Wrote {out_path}")

print("Done.")
