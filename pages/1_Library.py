import json
from pathlib import Path

import streamlit as st

import sys 
import os 
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OUTPUT_DIR, UPLOADS_DIR

from core.session_manager import (
    load_settings,
    save_settings
)

settings = load_settings()

if not settings["is_processed"]:

    st.warning(
        "Start a session first."
    )

    st.stop()
    

def get_papers():

    papers = []

    for folder in sorted(
        OUTPUT_DIR.iterdir()
    ):

        if not folder.is_dir():
            continue

        analysis_file = (
            folder
            / "paper_analysis.json"
        )

        if not analysis_file.exists():
            continue

        with open(
            analysis_file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        papers.append(
            {
                "paper_id": folder.name,
                "analysis": data
            }
        )

    return papers



st.title("Library")

papers = get_papers()

paper_ids = [
    paper["paper_id"]
    for paper in papers
]

selected = st.selectbox(
    "Select Document",
    paper_ids
)


paper = next(

    p
    for p in papers

    if p["paper_id"] == selected
)


analysis = paper["analysis"]

st.header(
    "Document Summary"
)

st.write(

    analysis.get(
        "paper_summary",
        "Not found"
    )
)


st.header(
    "Section Summaries"
)

section_summaries = (

    analysis.get(
        "section_summaries",
        {}
    )

)
# print(section_summaries)
for section in section_summaries:

    with st.expander(
        section["title"]
    ):
        st.write(
            section["summary"]
        )