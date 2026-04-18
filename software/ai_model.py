"""
ai_model.py
-----------
AI Text Generation Script for Emma AI Robot.
Uses Google Gemini API to generate intelligent responses.

Step 2: Text Generation using Gemini API
Get your API key from: https://ai.google.dev/gemini-api/docs/api-key

Libraries: google-generativeai, python-dotenv
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def gemini_api(text):
    """
    Sends input text to the Gemini API and returns the AI-generated response.

    :param text: The user's question or input string.
    :return:     The AI-generated response as a string.
    """
    model = genai.GenerativeModel(model_name="gemini-2.5-flash-latest")
    response = model.generate_content(text)
    print(response.text)
    return response.text  # Fixed: was missing return; also removed misplaced indentation


# ------------- MAIN -------------

if __name__ == "__main__":
    text = "2 + 2 is?"
    gemini_api(text)
