from summarize.generate_summary import main as summary_generator
from langchain_google_genai import ChatGoogleGenerativeAI
from extractor.extract_paper import main as paper_extractor
from flash_card.card_generator import execute as card_generator
from qa_chain.qa_chain import main as qa_chain

def run_pipeline(model_name, api_key, hf_token, language):
    llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.1,
        )
    
    paper_extractor(hf_token)
 
    summary_generator(llm, language)
    
    card_generator(llm, language)

    qa_chain(selected="")

