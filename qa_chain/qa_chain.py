import json
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OUTPUT_DIR, UPLOADS_DIR, CHROMA_DIR
from core.session_manager import (
    load_settings,
    save_settings
)



text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200
)


embedding_function = OllamaEmbeddings(
    model="embeddinggemma",
    base_url="http://localhost:11434",  # default, change if needed
)

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)
    

def build_documents(output_dir):

    splits = []

    output_dir = Path(output_dir)

    for paper_dir in output_dir.iterdir():

        if not paper_dir.is_dir():
            continue

        print(f"Processing {paper_dir.name}")

        # ----------------------------------
        # Sections
        # ----------------------------------

        sections_file = paper_dir / "root_sections.json"

        if sections_file.exists():

            sections_data = load_json(
                sections_file
            )

            paper_title = (
                sections_data
                .get("document_profile", {})
                .get("title", paper_dir.name)
            )

            paper_id = paper_dir.name

            sections = (
                sections_data
                .get("sections", {})
            )

            for section_title, content in sections.items():

                chunks = (
                    text_splitter
                    .split_text(content)
                )

                for chunk_idx, chunk in enumerate(chunks):

                    splits.append(

                        Document(

                            page_content=chunk,

                            metadata={

                                "type":
                                    "text_chunk",

                                "content_level":
                                    "fine",

                                "paper_id":
                                    paper_id,

                                "paper_title":
                                    paper_title,

                                "section_title":
                                    section_title,

                                "chunk_index":
                                    chunk_idx
                            }
                        )
                    )

        else:
            continue

        # ----------------------------------
        # Tables
        # ----------------------------------

        tables_file = paper_dir / "tables.json"

        if tables_file.exists():

            tables = load_json(
                tables_file
            )

            for table in tables:

                caption = table.get(
                    "caption",
                    ""
                )

                table_content = ""

                if "table_markdown" in table:

                    table_content = (
                        table["table_markdown"]
                    )

                elif "data" in table:

                    table_content = str(
                        table["data"]
                    )

                text = f"""
Caption:
{caption}

Table Content:
{table_content}
"""

                splits.append(

                    Document(

                        page_content=text,

                        metadata={

                            "type":
                                "table",

                            "content_level":
                                "fine",

                            "paper_id":
                                paper_id,

                            "paper_title":
                                paper_title,

                            "table_id":
                                table.get(
                                    "table_id",
                                    -1
                                ),

                            "label":
                                table.get(
                                    "table_label",
                                    ""
                                )
                        }
                    )
                )

        # ----------------------------------
        # Figures
        # ----------------------------------

        figures_file = paper_dir / "figures.json"

        if figures_file.exists():

            figures = load_json(
                figures_file
            )

            for figure in figures:

                caption = figure.get(
                    "caption",
                    ""
                )
                if caption == None:
                    continue
                print(caption)

                splits.append(

                    Document(

                        page_content=caption,

                        metadata={

                            "type":
                                "figure",

                            "content_level":
                                "fine",

                            "paper_id":
                                paper_id,

                            "paper_title":
                                paper_title,

                            "figure_id":
                                figure.get(
                                    "figure_id",
                                    -1
                                ),

                            "label":
                                figure.get(
                                    "figure_label",
                                    ""
                                )
                        }
                    )
                )

        # ----------------------------------
        # Paper Analysis
        # ----------------------------------

        analysis_file = (
            paper_dir /
            "paper_analysis.json"
        )

        if analysis_file.exists():

            analysis = load_json(
                analysis_file
            )

            # ==============================
            # Section Summaries
            # ==============================

            section_summaries = (
                analysis.get(
                    "section_summaries",
                    []
                )
            )

            for section in section_summaries:

                splits.append(

                    Document(

                        page_content=
                            section["summary"],

                        metadata={

                            "type":
                                "section_summary",

                            "content_level":
                                "coarse",

                            "paper_id":
                                paper_id,

                            "paper_title":
                                paper_title,

                            "section_title":
                                section.get(
                                    "title",
                                    ""
                                ),

                            "root_section":
                                section.get(
                                    "root_section",
                                    ""
                                )
                        }
                    )
                )

            # ==============================
            # Paper Summary
            # ==============================

            paper_summary = (
                analysis.get(
                    "paper_summary",
                    ""
                )
            )

            if paper_summary:

                splits.append(

                    Document(

                        page_content=
                            paper_summary,

                        metadata={

                            "type":
                                "paper_summary",

                            "content_level":
                                "coarse",

                            "paper_id":
                                paper_id,

                            "paper_title":
                                paper_title
                        }
                    )
                )
    return splits



def main( selected):

    settings = load_settings()

    db_name = settings["db_name"]
    persist_directory = os.path.join(
        CHROMA_DIR,
        db_name
    )


    # -------------------------------------
    # Load Existing DB
    # -------------------------------------
    
    if os.path.exists(persist_directory):

        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function,
            # collection_name = "my_collection"
        )
        print(f"vector store is loaded {db_name}")

    else:
        splits = build_documents(
            OUTPUT_DIR
        )
        print(f"vector store creating \t{db_name}")
        print(
            f"Total documents: {len(splits)}"
        )
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embedding_function,
            persist_directory=persist_directory,
            # collection_name = "my_collection"
        )
    retriever = vectorstore.as_retriever(search_kwargs={
        "k": 5,
        "filter": {
            "paper_id": selected
        }
    })
    
    return retriever
