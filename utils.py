import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

if not MISTRAL_API_KEY:
    raise ValueError("🚨 Mistral API key is missing! Please set it in a .env file.")

def generate_questions(tech, experience, model="mistral-medium", temperature=0.7, max_tokens=200):
    """
    Generate 3 technical interview questions using Mistral AI API.

    Args:
        tech (str): Technology for which questions should be generated.
        experience (str): Candidate's experience level.
        model (str): Mistral model to use (default: "mistral-medium").
        temperature (float): Randomness in responses.
        max_tokens (int): Maximum response length.

    Returns:
        str: A list of 3 generated technical questions.
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"Generate 3 technical interview questions about {tech} "
                            f"for a candidate with {experience} years of experience. "
                            "Format as a single, compact numbered list without unnecessary line breaks. "
                            "Ensure each question is on the same line as its number, and separate questions with ' ||| ' for clarity."

            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException as e:
        return f"HTTP Request Error: {str(e)}"
    except KeyError:
        return "Error: Unexpected response format from Mistral API."
