from pathlib import Path
import json
# from fig_caption import extract_figure_captions
from docling.document_converter import DocumentConverter
from huggingface_hub import login
import re
from extractor.table import process_output_folder as table_caption
from extractor.fig_caption import process_output_folder as fig_caption
from extractor.fig_caption import update_figure_ids

import sys 
import os 
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OUTPUT_DIR, UPLOADS_DIR





def save_text(doc, paper_dir):

    markdown_text = doc.export_to_markdown()

    (paper_dir / "text.md").write_text(
        markdown_text,
        encoding="utf-8"
    )




def process_pdf(pdf_path):

    converter = DocumentConverter()

    result = converter.convert(pdf_path)

    doc = result.document

    paper_name = Path(pdf_path).stem

    paper_dir = OUTPUT_DIR / paper_name

    paper_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    save_text(doc, paper_dir)

    print(f"Finished: {paper_name}")


def main(hf_token):

    login(token=hf_token)

    pdf_folder = Path(UPLOADS_DIR)

    OUTPUT_DIR.mkdir(exist_ok=True)

    for pdf_file in pdf_folder.glob("*.pdf"):
        print(pdf_file)
        process_pdf(str(pdf_file))
    
    output_dir = Path(OUTPUT_DIR)
    table_caption(output_dir)
    fig_caption(output_dir)

    for paper_dir in output_dir.iterdir():

        if not paper_dir.is_dir():
            continue

        json_file = paper_dir / "figures.json"

        if json_file.exists():

            update_figure_ids(json_file)

            print(
                f"Updated {json_file}"
            )



# main()