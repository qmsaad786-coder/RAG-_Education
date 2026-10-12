import google.generativeai as genai
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from .config import GOOGLE_API_KEY


def get_llm_runnable():
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-3.5-flash")

    def call_gemini(prompt_input):
        # 🔥 CRITICAL FIX
        # Ensure prompt is always plain string
        if isinstance(prompt_input, dict):
            prompt = str(prompt_input)
        else:
            prompt = str(prompt_input)

        response = model.generate_content(prompt)
        return response.text

    return RunnableLambda(call_gemini) | StrOutputParser()