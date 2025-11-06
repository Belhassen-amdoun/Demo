import re
import base64
from openai import OpenAI
import json
import os
import base64
import json
from openai import OpenAI

openai_api_key = "####################################"
client = OpenAI(api_key=openai_api_key)


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def call_openai_ocr(image_path: str):
    img_b64 = image_to_base64(image_path)
    data_uri = f"data:image/png;base64,{img_b64}"

    system_prompt = (
    "You are an assistant that reads an image containing an invoice or a receipt. "
    "Read all the text, extract the important information such as client, date, amount, currency, and description. "
    "Generate a natural paragraph summarizing the invoice. "
    "Return only a JSON object with the following structure: "
    "{"
    "  'client': '',"
    "  'date': '',"
    "  'amount': '',"
    "  'currency': '',"
    "  'description': '',"
    "  'paragraph': ''"
    "}"
    "Do not add any text outside this JSON."
)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyse cette image et retourne le JSON demandé."},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    
    try:
        data = json.loads(content)
    except Exception:
        data = {"paragraph": content}  

    return data
