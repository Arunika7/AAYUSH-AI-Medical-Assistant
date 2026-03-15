"""
app.py - AAYUSH entry point
----------------------------
Wires together all modules from the `aayush` package.
Keep this file thin: page config, state init, render components, handle events.

API key is loaded automatically from .env via aayush/config.py.
"""

import streamlit as st

# Page config must be the very first Streamlit call
st.set_page_config(
    page_title="AAYUSH - AI Medical Assistant",
    page_icon="assets/favicon.png" if __import__("os").path.exists("assets/favicon.png") else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Internal imports ──────────────────────────────────────────────────────────
from aayush.ui.styles      import inject_styles
from aayush.ui.sidebar     import render_sidebar
from aayush.ui.chat        import render_header, render_chat_history
from aayush.ui.input_panel import render_input_panel
from aayush.gemini_client  import generate_response
from aayush.image_utils    import pil_to_bytes
from aayush.config         import GOOGLE_API_KEY
from aayush               import state

# ── Bootstrap ─────────────────────────────────────────────────────────────────
inject_styles()
state.init_state()

# Fail clearly at startup if the API key is missing
if not GOOGLE_API_KEY:
    st.error(
        "**GOOGLE_API_KEY not found.**  \n"
        "Create a `.env` file in the project root and add your key:\n\n"
        "```\nGOOGLE_API_KEY=AIza...\n```",
        icon=None,
    )
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar = render_sidebar()

if sidebar["clear_clicked"]:
    state.clear_chat()
    st.rerun()

# ── Main content ──────────────────────────────────────────────────────────────
render_header()
render_chat_history(st.session_state.messages)

# ── Input panel ───────────────────────────────────────────────────────────────
panel = render_input_panel()

# ── Handle send ───────────────────────────────────────────────────────────────
if panel["send"]:
    query    = panel["query"].strip()
    uploaded = panel["uploaded"]
    pil_img  = panel["pil_img"]

    if not query and uploaded is None:
        st.warning("Please type a question or upload an image (or both).")
        st.stop()

    # Record user message
    user_display = query or "(Image analysis request)"
    state.add_message("user", user_display)
    state.increment_queries()

    # Build multimodal parts list for Gemini
    parts: list = []
    if pil_img is not None:
        img_bytes = pil_to_bytes(pil_img)
        parts.append({"mime_type": "image/png", "data": img_bytes})
        state.increment_images()
        if not query:
            parts.append("Please provide a detailed radiological analysis of this medical image.")
    if query:
        parts.append(query)

    # Call Gemini
    with st.spinner("AAYUSH is analysing..."):
        try:
            answer = generate_response(st.session_state.messages, parts)
            state.add_message("assistant", answer)
        except Exception as exc:
            err = str(exc)
            # Roll back the optimistic user message
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                st.session_state.messages.pop()

            if "QUOTA" in err.upper() or "429" in err:
                st.error("API quota exceeded. Please wait a moment and try again.")
            else:
                st.error(f"Error: {err}")
            st.stop()

    st.rerun()
