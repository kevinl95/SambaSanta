import boto3
from openai import OpenAI
import os

def handler(event, context):
    print(event)
    text = event.get("text")
    api_key = os.environ.get("SAMBANOVA_API_KEY")

    client = OpenAI(
        base_url="https://api.sambanova.ai/v1/",
        api_key=api_key,  
    )

    model = "Meta-Llama-3.1-405B-Instruct"
    prompt = "Pretend you are Santa and write a letter intended for a child based on this letter they have sent you: " + text

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user", 
                "content": prompt,
            }
        ],
        stream=True,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    print(response)
    return {"result": response}