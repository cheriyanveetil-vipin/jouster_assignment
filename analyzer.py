import os, json
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def analyze_text(text: str) -> Dict:

    if not text or not text.strip():
        return {"error": "Empty text provided"}

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY not set"}

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are an assistant that extracts insights from text.
    Given the following text, return a JSON object with two fields:
    1. "summary": a short summary of the text
    2. "structured_data": an object with keys "title", "topics", and "sentiment"

    Text:
    {text}
    """

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.0
        )
        content = resp.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}
