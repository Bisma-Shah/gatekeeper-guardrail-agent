from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI-API-KEY")

# Raise an error if API key is missing
if not gemini_api_key:
    raise ValueError("GEMINI-API-KEY is not set. Please ensure it is defined in your .env file.")

# Initialize the external client for Gemini API
# Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define the model using Gemini (OpenAI compatible interface)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Create the final run configuration used by agents
config = RunConfig(
    model=model,
    model_provider=external_client,
)
