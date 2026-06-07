from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = ROOT_DIR / "outputs"

CHROMA_DIR = ROOT_DIR / "vector_db"

UPLOADS_DIR = ROOT_DIR / "inputs/papers"

GRAPH_DIR = OUTPUT_DIR / "graph"

SUMMARY_DIR = OUTPUT_DIR / "summarize"

QA_DIR = OUTPUT_DIR / "qa_chain"

EXTRACTOR_DIR = OUTPUT_DIR / "extractor"