import json
import re
from pathlib import Path
import hashlib

SUPPLEMENTARY_OFFSET = 1000

ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def roman_to_int(roman: str) -> int:

    roman = roman.upper()

    total = 0
    prev = 0

    for char in reversed(roman):

        value = ROMAN_VALUES[char]

        if value < prev:
            total -= value
        else:
            total += value
            prev = value

    return total


TABLE_CAPTION_PATTERN = re.compile(
    r"^(table\s+[a-z0-9\-\.]+.*)$",
    re.IGNORECASE
)

TABLE_ID_PATTERN = re.compile(
    r"table\s+([A-Za-z]?[A-Za-z0-9]+)",
    re.IGNORECASE
)


def is_table_line(line: str) -> bool:

    line = line.strip()

    if not line:
        return False

    indicators = [
        "|",
        "---",
        ":--",
        "--:",
        "+-",
        "-+"
    ]

    return any(
        indicator in line
        for indicator in indicators
    )


SUPPLEMENTARY_OFFSET = 1000


def parse_table_id(caption):

    if not caption:
        return -1, None

    match = TABLE_ID_PATTERN.search(
        caption
    )

    if not match:
        return -1, None

    label = match.group(1).upper()

    # -----------------
    # Supplementary
    # -----------------

    if label.startswith("S"):

        raw = label[1:]

        if raw.isdigit():

            return (
                SUPPLEMENTARY_OFFSET + int(raw),
                label
            )

        try:

            value = roman_to_int(raw)

            return (
                SUPPLEMENTARY_OFFSET + value,
                label
            )

        except Exception:

            return -1, label

    # -----------------
    # Normal numeric
    # -----------------

    if label.isdigit():

        return int(label), label

    # -----------------
    # Roman numerals
    # -----------------

    try:

        value = roman_to_int(label)

        return value, label

    except Exception:

        return -1, label






def remove_duplicate_tables(tables):

    grouped = {}

    for table in tables:

        signature = hashlib.md5(
            table["table_markdown"]
            .strip()
            .encode("utf-8")
        ).hexdigest()

        distance = abs(
            table["table_start_line"]
            - table["caption_line"]
        )

        if signature not in grouped:

            grouped[signature] = table
            grouped[signature]["_distance"] = (
                distance
            )

            continue

        current_best = grouped[
            signature
        ]

        if distance < current_best["_distance"]:

            table["_distance"] = distance

            grouped[signature] = table

    result = []

    for table in grouped.values():

        table.pop(
            "_distance",
            None
        )

        result.append(table)
    result = [
        table
        for table in result
        if "_distance" not in table
    ]
    print(len(result))

    return result

def extract_tables_from_markdown(md_text):

    lines = md_text.splitlines()

    tables = []

    for idx, line in enumerate(lines):

        line = line.strip()

        if not TABLE_CAPTION_PATTERN.match(
            line
        ):
            continue

        caption = line

        table_start = None

        search_start = max(
            0,
            idx - 3
        )

        search_end = min(
            len(lines),
            idx + 40
        )

        for pos in range(
            search_start,
            search_end
        ):

            if is_table_line(
                lines[pos]
            ):

                table_start = pos
                break

        if table_start is None:
            continue

        table_lines = []

        pos = table_start

        empty_count = 0

        while pos < len(lines):

            current = lines[pos]

            if current.strip() == "":

                empty_count += 1

                if empty_count >= 2:
                    break

                table_lines.append(
                    current
                )

                pos += 1
                continue

            empty_count = 0

            if not is_table_line(
                current
            ):
                break

            table_lines.append(
                current
            )

            pos += 1

        table_id, table_label = (
            parse_table_id(caption)
        )

        tables.append(
            {
                "table_id": table_id,
                "table_label": table_label,
                "caption": caption,
                "table_markdown": "\n".join(
                    table_lines
                ),
                "table_start_line":table_start,
                "caption_line": idx
            }
        )
    tables = remove_duplicate_tables(tables)

    return tables


def process_output_folder(output_dir):


    for paper_dir in output_dir.iterdir():

        if not paper_dir.is_dir():
            continue

        md_file = paper_dir / "text.md"

        if not md_file.exists():
            continue

        print(
            f"Processing: {paper_dir.name}"
        )

        md_text = md_file.read_text(
            encoding="utf-8"
        )

        tables = extract_tables_from_markdown(
            md_text
        )

        output_file = (
            paper_dir / "tables.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                tables,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(
            f"Found {len(tables)} tables"
        )
