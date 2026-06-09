import streamlit as st
import sys 
import os 
from pathlib import Path
import shutil
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OUTPUT_DIR, UPLOADS_DIR, CHROMA_DIR

from pipeline import run_pipeline
from core.session_manager import (
    load_settings,
    save_settings
)


settings = load_settings()

    
model_name = st.selectbox(
    "Model",
    [
        "gemini-3.1-flash-lite",
        "gemini-3-flash-preview",
        "gemini-3-pro",
    ]
)

language = st.selectbox(
    "Language",
    [
        "English",
        "Deutch",
        "Persian",
        "Latin"
    ]
)

google_api_key = st.text_input(
    "Google API Key",
    type="password"
)

hf_token = st.text_input(
    "HF Token",
    type="password"
)

uploaded_files = st.file_uploader(
    "Upload Papers",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button(
    "Start Session"
):
        db_name = datetime.now().strftime(
            "chroma_%Y%m%d_%H%M%S"
        )
        settings = {

        "llm_provider":
            "google",

        "llm_model":
            model_name,

        "embedding_model":
            "embeddinggemma",

        "google_api_key":
            google_api_key,

        "hf_token":
            hf_token,
        
        "language":
            language,
        
        "db_name":
            db_name,

        "is_processed":
            False
    }
        
        save_settings(
            settings
        )
    

        UPLOADS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        for file in uploaded_files:
        
            save_path = (
                UPLOADS_DIR
                / file.name
            )

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(
                    file.getbuffer()
                )

        chroma_dir = Path(CHROMA_DIR)
        if chroma_dir.exists() and chroma_dir.is_dir():
            for item in chroma_dir.iterdir():          # iterate over contents
                if item.is_dir() and item.name != db_name:
                    try:
                        shutil.rmtree(item)
                    except Exception as e:
                        print(f"Failed to remove {item}: {e}")

        run_pipeline(model_name, google_api_key, hf_token, language)

        settings["is_processed"] = True
        st.success("Now your system is ready.")

        save_settings(
            settings
    )



# if st.button("Restart Session"):
#     st.session_state["confirm_restart"] = True

# if st.session_state.get("confirm_restart"):

#     st.warning(
#         "This will delete all current session data."
#     )

#     col1, col2 = st.columns(2)

#     with col1:

#         if st.button("Yes, Delete Everything"):

#             reset_session()

#             st.session_state["confirm_restart"] = False

#             st.success(
#                 "Session restarted."
#             )

#             st.rerun()

#     with col2:

#         if st.button("Cancel"):

#             st.session_state["confirm_restart"] = False

#             st.rerun()
def reset_session():

    folders = [
        Path("inputs/papers"),
        Path("outputs"),
        Path("vector_db/chroma_db"),
    ]

    for folder in folders:
        if folder.exists():
            print(folder)
            try:
                shutil.rmtree(
                    folder
                )
            except:
                pass

    settings_file = Path(
        "session/settings.json"
    )

    if settings_file.exists():

        settings_file.unlink()   

if st.button("Restart Session"):
    st.session_state["confirm_restart"] = True

if st.session_state.get("confirm_restart"):

    st.warning(
        "This will delete all current session data."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Yes, Delete Everything"):

            reset_session()

            st.session_state["confirm_restart"] = False

            st.success(
                "Session restarted."
            )

            st.rerun()

    with col2:

        if st.button("Cancel"):

            st.session_state["confirm_restart"] = False

            st.rerun()

# # دکمه ریستارت
# if st.button("Restart Session"):
#     st.session_state["confirm_restart"] = True

# if st.session_state.get("confirm_restart"):
#     st.warning("This will delete all current session data.")
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Yes, Delete Everything"):
#             # به جای حذف فوری، پرچم می‌گذاریم و ریلود می‌کنیم
#             st.session_state["do_reset"] = True
#             st.session_state["confirm_restart"] = False
#             st.rerun()
#     with col2:
#         if st.button("Cancel"):
#             st.session_state["confirm_restart"] = False
#             st.rerun()