import streamlit as st
from qa_chain.qa_chain import main as answer_question
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

import json
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
llm = ChatGoogleGenerativeAI(
            model=settings["llm_model"],
            google_api_key=settings["google_api_key"],
            temperature=0.1,
        )
st.title(
    "Document Chat"
)
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




papers = get_papers()

paper_ids = [
    paper["paper_id"]
    for paper in papers
]

selected = st.selectbox(
    "Select Document",
    paper_ids
)

question = st.chat_input(
    "Ask a question..."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
answer {language} in and keep it concise."""),
    ("human", """Question: {question}
Context: {context}
Answer:""")
])


# del qa_chain

if question:
    retriever = answer_question(selected)
    
    qa_chain = (
        {"context": retriever,"language": RunnablePassthrough(), "question":RunnablePassthrough()}
        | prompt
        | llm
    )

    with st.chat_message(
        "user"
    ):
        st.write(question)

    answer = qa_chain.invoke(
        question
    )
    # answer = "hello i am a human"
    
    with st.chat_message(
        "assistant"
    ):
        st.write(answer.content[0]["text"])
        # st.write(answer)

        