import os
from groq import Groq
from dotenv import load_dotenv
from app.utils.retry import retry

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_llm_response(prompt:str):
    def call():
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b"
        )
        return response.choices[0].message.content

    return retry(call, retries=3, delay=2)