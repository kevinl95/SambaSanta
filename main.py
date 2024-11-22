import boto3
from openai import OpenAI
import os

def handler(event, context):
    text = event.get("text")
    api_key = os.environ.get("SAMBANOVA_API_KEY")

    # Get the SNS Topic ARN from the environment variable
    sns_topic_arn = os.getenv('SNS_TOPIC_ARN')

    # Create an SNS client
    sns_client = boto3.client('sns')

    client = OpenAI(
        base_url="https://api.sambanova.ai/v1/",
        api_key=api_key,  
    )

    model = "Meta-Llama-3.1-405B-Instruct"
    prompt = "Pretend you are Santa and write a letter intended for a child (do not include the child's name unless they specify it or anything in brackets) based on this letter they have sent you: " + text

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

    # Publish the response letter to the topic
    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=response,
        Subject="Merry Christmas from Santa!"
    )
    return {"result": response}
