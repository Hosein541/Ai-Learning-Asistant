import json
from pathlib import Path

import streamlit as st
import json
import sys 
import os 
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
            / "flashcards.json"
        )

        if not analysis_file.exists():
            continue

        papers.append(
            {
                "paper_id": folder.name,
            }
        )

    return papers



# st.title("Library")

papers = get_papers()

paper_ids = [
    paper["paper_id"]
    for paper in papers
]

selected = st.selectbox(
    "Select Ducoment",
    paper_ids
)



FLASHCARD_FILE = Path(
    f"{OUTPUT_DIR}/{selected}/flashcards.json"
)


# @st.cache_data
def load_flashcards():

    with open(
        FLASHCARD_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


cards = load_flashcards()

if not cards:

    st.warning(
        "No flashcards found."
    )

    st.stop()


# ----------------------------------
# Session State
# ----------------------------------

if "current_card" not in st.session_state:

    st.session_state.current_card = 0

if "show_answer" not in st.session_state:

    st.session_state.show_answer = False


# ----------------------------------
# Current Card
# ----------------------------------

current_index = st.session_state.current_card
try :
    card = cards[current_index]
except :
    card = cards[0]

# ----------------------------------
# Layout
# ----------------------------------

left_col, main_col = st.columns(
    [1, 3]
)


# ==================================
# Sidebar Card List
# ==================================

with left_col:

    st.subheader(
        "Cards"
    )

    for idx, c in enumerate(cards):

        if st.button(
            f"{idx + 1}",
            key=f"card_{idx}",
            use_container_width=True
        ):

            st.session_state.current_card = idx

            st.session_state.show_answer = False

            st.rerun()


# ==================================
# Main Card
# ==================================

with main_col:

    st.title(
        "Flashcards"
    )

    st.caption(
        card.get(
            "section_title",
            ""
        )
    )

    st.markdown("---")

    if not st.session_state.show_answer:

        st.markdown(
            f"""
            <div style="
                height:300px;
                border:2px solid #666;
                border-radius:15px;
                display:flex;
                align-items:center;
                justify-content:center;
                text-align:center;
                padding:20px;
                font-size:24px;
            ">
            {card["question"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Show Answer"
        ):

            st.session_state.show_answer = True

            st.rerun()

    else:

        st.markdown(
            f"""
            <div style="
                height:300px;
                border:2px solid #666;
                border-radius:15px;
                display:flex;
                align-items:center;
                justify-content:center;
                text-align:center;
                padding:20px;
                font-size:22px;
            ">
            {card["answer"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Back To Question"
        ):

            st.session_state.show_answer = False

            st.rerun()


    st.markdown("---")

    prev_col, next_col = st.columns(2)

    with prev_col:

        if st.button(
            "⬅ Previous",
            use_container_width=True
        ):

            st.session_state.current_card = max(
                0,
                current_index - 1
            )

            st.session_state.show_answer = False

            st.rerun()

    with next_col:

        if st.button(
            "Next ➡",
            use_container_width=True
        ):

            st.session_state.current_card = min(
                len(cards) - 1,
                current_index + 1
            )
            if st.session_state.current_card == len(cards) - 1:
                st.session_state.current_card = 0


            st.session_state.show_answer = False

            st.rerun()


    st.caption(
        f"Card {current_index + 1} / {len(cards)}"
    )