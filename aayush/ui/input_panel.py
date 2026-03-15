"""
aayush/ui/input_panel.py
─────────────────────────
Renders the two-column input area:
  - Left  : file uploader + image preview
  - Right : text area + Send / Clear buttons

Returns a dict the main loop uses to trigger generation.
"""

import streamlit as st

from aayush.config import ALLOWED_IMAGE_TYPES
from aayush.image_utils import preprocess_image
from aayush import state


def render_input_panel() -> dict:
    """
    Draw the upload + query input area.

    Returns:
        {
            "send":     bool          - True when the Send button was clicked,
            "query":    str           - The text the user typed,
            "uploaded": UploadedFile  - The file widget value (or None),
            "pil_img":  PIL.Image     - Preprocessed image (or None),
        }
    """
    result = {"send": False, "query": "", "uploaded": None, "pil_img": None}

    col_img, col_chat = st.columns([1, 2], gap="large")

    # ── Left: image upload ────────────────────────────────────────────────────
    with col_img:
        st.markdown("**Upload Medical Image**")
        uploaded = st.file_uploader(
            "X-ray | MRI | CT | Ultrasound",
            type=ALLOWED_IMAGE_TYPES,
            label_visibility="collapsed",
        )
        if uploaded:
            pil_img = preprocess_image(uploaded)
            st.image(pil_img, caption=uploaded.name, use_container_width=True)
            st.caption(f"Preprocessed: {pil_img.size[0]} x {pil_img.size[1]} px  |  RGB")
            result["uploaded"] = uploaded
            result["pil_img"]  = pil_img

    # ── Right: text query ─────────────────────────────────────────────────────
    with col_chat:
        st.markdown("**Your Question**")

        # Consume any pending quick-prompt text
        default_text = state.pop_quick_prompt()

        user_query = st.text_area(
            "Query",
            value=default_text,
            height=120,
            placeholder=(
                "e.g. What abnormalities are visible in this chest X-ray?\n"
                "or ask any clinical / pharmacological question..."
            ),
            label_visibility="collapsed",
            key="query_input",
        )

        col_send, col_clr = st.columns([3, 1])
        with col_send:
            if st.button("Send to AAYUSH", use_container_width=True, type="primary"):
                result["send"] = True
        with col_clr:
            if st.button("Clear", use_container_width=True):
                state.set_quick_prompt("")
                st.rerun()

        result["query"] = user_query

    return result
