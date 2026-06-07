FLASHCARD_PROMPT = """
You are an educational flashcard generator.

Create high-quality study flashcards from the provided content.

Rules:
- Generate between {num_cards} flashcards.
- Every answer MUST be supported by the provided content.
- Questions should test understanding and recall.
- Avoid duplicate questions.
- Keep answers concise but complete.
- Return ONLY valid JSON.
- Create in {language} Language

Output format:

[
  {{
    "question": "...",
    "answer": "..."
  }}
]

Content:
{content}
"""



import json
import re
import os 
import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OUTPUT_DIR
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


def extract_json(text):

    text = text.strip()

    if text.startswith("```json"):
        text = re.sub(
            r"^```json",
            "",
            text
        )

        text = re.sub(
            r"```$",
            "",
            text
        )

    return json.loads(text)


def generate_section_flashcards(
    llm,
    block,
    language,
    num_cards=3
):

    prompt = ChatPromptTemplate.from_template(
        FLASHCARD_PROMPT
    ) 
    chain =(
            prompt
            | llm)
    response = chain.invoke({"num_cards": num_cards, "content": block["content"], "language": language})
    print(response)
    cards = extract_json(
        response.content[0]["text"]
    )

    result = []

    for idx, card in enumerate(cards):

        result.append(
            {
                "card_id": idx + 1,
                "root_section":
                    block["root_section"],

                "section_title":
                    block["title"],

                "question":
                    card["question"],

                "answer":
                    card["answer"]
            }
        )

    return result


def generate_flashcards(
    summary_blocks,
    llm,
    language,
    cards_per_section=3
):

    all_cards = []

    global_id = 1

    for block in summary_blocks:

        cards = generate_section_flashcards(
            llm=llm,
            block=block,
            num_cards=cards_per_section,
            language=language
        )

        for card in cards:

            card["card_id"] = global_id

            global_id += 1

            all_cards.append(card)

    return all_cards



def save_flashcards(
    output_dir,
    flashcards
):

    output_file = os.path.join(
        output_dir,
        "flashcards.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            flashcards,
            f,
            indent=2,
            ensure_ascii=False
        )


import json
import os


def execute(
    llm, 
    language
):
    for paper_dir in OUTPUT_DIR.iterdir():

        if not paper_dir.is_dir():
            continue

        summary_file = paper_dir / "summary_blocks.json"
        if summary_file.exists() and summary_file.is_file():

            with open(
                summary_file,
                "r",
                encoding="utf-8"
            ) as f:

                summary_blocks = json.load(f)
        else :
            print(f"Warning: The file '{summary_file}' was not found or is not a regular file.")
            continue
        flashcards = generate_flashcards(
            summary_blocks,
            llm,
            language
        )

        save_flashcards(
            paper_dir,
            flashcards
        )

    # return flashcards


# llm = ChatGoogleGenerativeAI(
#             model="gemini-3.1-flash-lite",
#             google_api_key="AIzaSyDYuiX0iPytcXR4HopRwyT1kUoBOeWm_dM",
#             temperature=0.15,
#         )
# execute(llm)