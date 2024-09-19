import os

from enum import Enum
import openai
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key is not set. Please set the 'OPENAI_API_KEY' in the .env file.")

MODEL = "gpt-4o-2024-08-06"

client = OpenAI(api_key=api_key)


# ----------------------------------------------------------------------
# Example 1 : Basic example that extracts the event info from user input
# ----------------------------------------------------------------------

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def extract_event_information() -> CalendarEvent:
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}
        ],
        response_format=CalendarEvent
    )
    return completion.choices[0].message.parsed


print(extract_event_information())


# ----------------------------------------------------------------------
# Example 2 : Enums example : Sentiment Analysis
# ----------------------------------------------------------------------

class SentimentCategory(str, Enum):
    POSITIVE = "positive",
    NEGATIVE = "negative"


class Reply(BaseModel):
    content: str = Field(description="Your reply that we send to the customer.")
    category: SentimentCategory
    confidence: float = Field(
        description="Confidence in the category prediction."
    )


def do_sentiment_analysis() -> Reply:
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system",
             "content": "You will be given a customer query and you have to categorise in a positive or negative sentiment"},
            {"role": "user", "content": "Your products are amazing"}
        ],
        response_format=Reply
    )
    return completion.choices[0].message.parsed


print(do_sentiment_analysis())

# JSON is one of the most widely used formats in the world for applications
# to exchange data.
# Structured Outputs is a feature that ensures the model will always generate
# responses that adhere to your supplied JSON Schema, so you don't need to worry
# about the model omitting a required key, or hallucinating an invalid enum value

# Tested code on openai 1.46.0 and python 3.12.4
