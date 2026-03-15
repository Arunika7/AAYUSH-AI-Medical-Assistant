"""
aayush/gemini_client.py
────────────────────────
Gemini API interaction: model initialisation, chat history conversion,
and the response-generation call.

The API key is loaded once from config (via .env) — it is never
exposed in the UI or passed at runtime.
"""

import streamlit as st
import google.generativeai as genai

from aayush.config import (
    GOOGLE_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    TOP_P,
    MAX_OUTPUT_TOKENS,
    SAFETY_SETTINGS,
    SYSTEM_PROMPT,
)


@st.cache_resource(show_spinner=False)
def get_model(_model_name: str = MODEL_NAME) -> genai.GenerativeModel:
    """Initialise and cache the Gemini GenerativeModel using the .env API key.
    The cache is keyed on _model_name so it auto-busts if the model changes.
    """
    genai.configure(api_key=GOOGLE_API_KEY)

    generation_config = genai.GenerationConfig(
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )

    return genai.GenerativeModel(
        model_name=_model_name,
        generation_config=generation_config,
        safety_settings=SAFETY_SETTINGS,
        system_instruction=SYSTEM_PROMPT,
    )


def build_gemini_history(messages: list) -> list:
    """
    Convert the app's flat message list into the format expected by
    `model.start_chat(history=...)`.

    Excludes the most-recent message (the one we're about to send) and
    skips image-bearing turns to avoid re-sending raw bytes each turn.
    """
    history = []
    for msg in messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        if isinstance(msg["content"], str):
            history.append({"role": role, "parts": [msg["content"]]})
    return history


def generate_response(messages: list, parts: list) -> str:
    """
    Send `parts` (text and/or image bytes) to Gemini and return the
    full response text. Retries automatically on quota / rate-limit errors
    with exponential backoff (up to 3 attempts).
    """
    import time

    model   = get_model(MODEL_NAME)
    history = build_gemini_history(messages)
    chat    = model.start_chat(history=history)

    wait_times = [5, 15, 30]   # seconds between retries
    last_exc: Exception = RuntimeError("Unknown error")

    for attempt, wait in enumerate([0] + wait_times):
        if wait:
            time.sleep(wait)
        try:
            response = chat.send_message(parts)
            return response.text
        except Exception as exc:
            last_exc = exc
            err = str(exc).upper()
            # Only retry on quota / rate-limit errors
            if "QUOTA" in err or "429" in err or "RESOURCE_EXHAUSTED" in err:
                if attempt < len(wait_times):
                    continue   # wait and retry
            raise  # non-quota error → surface immediately

    raise last_exc  # all retries exhausted
