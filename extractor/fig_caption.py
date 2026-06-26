import re
from pathlib import Path
import json




def extract_figure_captions(markdown_text: str):

    IMAGE_TAG = "<!-- image -->"


    CAPTION_PATTERN = re.compile(
        r"^(fig(?:ure)?\.?\s+[A-Za-z0-9\-\.]+.*)$",
        re.IGNORECASE
    )

    lines = markdown_text.splitlines()

    figures = []

    figure_id = 0

    for idx, line in enumerate(lines):

        if IMAGE_TAG not in line:
            continue

        caption = None

        for offset in range(1, 4):

            pos = idx - offset

            if pos < 0:
                break

            candidate = lines[pos].strip()

            if CAPTION_PATTERN.match(candidate):

                caption = candidate
                break

        if caption is None:

            for offset in range(1, 4):

                pos = idx + offset

                if pos >= len(lines):
                    break

                candidate = lines[pos].strip()

                if CAPTION_PATTERN.match(candidate):

                    caption = candidate
                    break

        figures.append(
            {
                "figure_id": figure_id,
                "caption": caption
            }
        )

        figure_id += 1

    return figures


def process_output_folder(output_dir):

    # output_dir = Path("output")

    for paper_dir in output_dir.iterdir():

        if not paper_dir.is_dir():
            continue

        md_file = paper_dir / "text.md"

        if not md_file.exists():
            continue

        md_text = md_file.read_text(
            encoding="utf-8"
        )

        figures = extract_figure_captions(md_text)

        with open(
            paper_dir / "figures.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                figures,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(
            f"{paper_dir.name}: {len(figures)} figures"
        )






def parse_figure_id(caption):
    ID_PATTERN = re.compile(
    r"fig(?:ure)?\.?\s+([A-Za-z]?\d+)",
    re.IGNORECASE
)

    match = ID_PATTERN.search(caption)

    if not match:
        return -1, None

    label = match.group(1).upper()

    # S6
    if label.startswith("S"):

        number = int(
            re.search(r"\d+", label).group()
        )

        return 100 + number, label

    # Figure 6
    number = int(
        re.search(r"\d+", label).group()
    )

    return number, label


def update_figure_ids(json_file):

    with open(
        json_file,
        "r",
        encoding="utf-8"
    ) as f:

        figures = json.load(f)

    for fig in figures:

        caption = fig.get("caption")
    
        if not caption:
        
            fig["figure_id"] = -1
            fig["figure_label"] = None
            continue
        
        figure_id, figure_label = parse_figure_id(
            caption
        )
    
        fig["figure_id"] = figure_id
        fig["figure_label"] = figure_label

    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            figures,
            f,
            indent=2,
            ensure_ascii=False
        )


