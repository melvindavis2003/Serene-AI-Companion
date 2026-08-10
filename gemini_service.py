import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

SYSTEM_INSTRUCTION = (
    "You are Serene, a gentle, empathetic, and warm AI emotional companion. "
    "Listen carefully to the user's voice message or prompt, understand their feelings and intent, "
    "and respond with a comforting, supportive, and conversational tone. "
    "Keep your response concise (around 50 to 100 words) so it sounds natural when spoken aloud. "
    "Do not use markdown formatting like asterisks or bold text, as your response will be read by Text-to-Speech."
)

def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is missing or invalid. Please set your GEMINI_API_KEY in the .env file."
        )
    return genai.Client(api_key=api_key)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

def process_audio_prompt(audio_bytes: bytes, mime_type: str = "audio/wav") -> str:
    """
    Sends raw audio bytes directly to Google Gemini 1.5 Flash for multimodal processing.
    Returns the AI companion's text response.
    """
    client = get_client()
    
    audio_part = types.Part.from_bytes(
        data=audio_bytes,
        mime_type=mime_type
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                SYSTEM_INSTRUCTION,
                audio_part,
                "Please respond to my voice message."
            ]
        )
        return response.text
    except Exception as e:
        if "404" in str(e) or "NOT_FOUND" in str(e):
            # Fallback to gemini-1.5-flash if custom model not found
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=[
                    SYSTEM_INSTRUCTION,
                    audio_part,
                    "Please respond to my voice message."
                ]
            )
            return response.text
        raise e

def process_text_prompt(prompt_text: str) -> str:
    """
    Processes plain text prompt using Gemini 1.5 Flash.
    """
    client = get_client()
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                SYSTEM_INSTRUCTION,
                prompt_text
            ]
        )
        return response.text
    except Exception as e:
        if "404" in str(e) or "NOT_FOUND" in str(e):
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=[
                    SYSTEM_INSTRUCTION,
                    prompt_text
                ]
            )
            return response.text
        raise e

if __name__ == "__main__":
    try:
        print("Testing Gemini Service connection...")
        res = process_text_prompt("Hello Serene, I had a busy day today.")
        print(f"Serene Response: {res}")
    except Exception as e:
        print(f"Configuration test result: {e}")
