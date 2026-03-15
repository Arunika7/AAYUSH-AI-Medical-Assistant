"""
aayush/state.py
────────────────
Streamlit session-state initialisation and helper accessors.

All default values live here so they are never scattered across UI files.
The API key is NOT part of session state — it is loaded from .env via config.py.
"""

import streamlit as st


# ── Defaults ───────────────────────────────────────────────────────────────────
_DEFAULTS: dict = {
    "messages":      [],       # List[{role: str, content: str}]
    "total_queries": 0,
    "total_images":  0,
    "quick_prompt":  "",
}


def init_state() -> None:
    """Initialise all session-state keys to their defaults (idempotent)."""
    for key, value in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ── Message helpers ────────────────────────────────────────────────────────────
def add_message(role: str, content: str) -> None:
    """Append a message dict to the chat history."""
    st.session_state.messages.append({"role": role, "content": content})


def clear_chat() -> None:
    """Reset conversation and quick-prompt state."""
    st.session_state.messages = []
    st.session_state.quick_prompt = ""


# ── Counter helpers ────────────────────────────────────────────────────────────
def increment_queries() -> None:
    st.session_state.total_queries += 1


def increment_images() -> None:
    st.session_state.total_images += 1


# ── Quick-prompt helpers ───────────────────────────────────────────────────────
def pop_quick_prompt() -> str:
    """Return the pending quick-prompt text and clear it from state."""
    value = st.session_state.get("quick_prompt", "")
    st.session_state.quick_prompt = ""
    return value


def set_quick_prompt(text: str) -> None:
    st.session_state.quick_prompt = text
