import os
import requests
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("API key is not set. Please set the 'OPENAI_API_KEY' in the .env file.")

MODEL = "gpt-3.5-turbo-0125"
client = OpenAI(api_key=API_KEY)

def get_available_domains(domain_names: list[str]) -> list[str]:
    available_domains = []
    for domain in domain_names:
        # Replace with actual API call to check domain availability
        if is_domain_available(domain):  
            available_domains.append(domain)
    return available_domains


def is_domain_available(domain: str) -> bool:
    # Here, you would implement the actual logic to check domain availability
    return True  


def get_domain_suggestions() -> dict:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_available_domains",
                "description": "Function that takes a list of domain names and returns those that are available.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "A list of domain names to check for availability."
                        },
                    },
                    "required": ["domain_names"],
                    "additionalProperties": False,
                },
            },
        }
    ]

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system",
             "content": "You are a helpful domain name generation expert. Use the supported tools to assist the user"},
            {"role": "user",
             "content": "Please suggest a single list of 10 domain names for an edtech startup"}
        ],
        tools=tools,
        tool_choice="auto"
    )
    return completion.choices[0].message

def extract_domain_names(arguments: str) -> list[str]:
    return json.loads(arguments)["domain_names"]


if __name__ == "__main__":
    assistant_response = get_domain_suggestions()
    print("Assistant Response:", assistant_response)
    
    if assistant_response.tool_calls:
        for tool_call in assistant_response.tool_calls:
            function_name = tool_call.function.name
            function_args = tool_call.function.arguments
            # Print function name and arguments
            print(f"Function Name: {function_name}")
            print(f"Function Arguments: {function_args}")
            
            # Call the appropriate function dynamically
            if function_name == "get_available_domains":
              domain_names = extract_domain_names(function_args)
              available_domains = get_available_domains(domain_names)
              print("Available domains from suggestions:", available_domains)
            else:
                print("Function name not recognized")
    else:
        print("No domain suggestions returned.")



