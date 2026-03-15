"""
aayush/ui/sidebar.py
─────────────────────
Renders the sidebar: logo, status pill, session statistics,
quick-prompt buttons, model info, clear button, and disclaimer.

The API key is loaded from .env — there is no user-facing key input here.
"""

import streamlit as st

from aayush.config import MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS, QUICK_PROMPTS
from aayush import state


def render_sidebar() -> dict:
    """
    Draw the sidebar and return a dict of user actions:
        { "clear_clicked": bool }
    """
    result = {"clear_clicked": False}

    with st.sidebar:
        # ── Logo & title ──────────────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding: 1.5rem 0 1rem;">
            <div style="font-size:1.3rem; font-weight:800;
                        background:linear-gradient(90deg,#60a5fa,#22d3ee);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;">
                AAYUSH
            </div>
            <div style="font-size:0.72rem; color:#64748b; margin-top:2px;">AI Medical Assistant</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="status-pill"><div class="status-dot"></div>'
            'Gemini 2.0 Flash &nbsp;&middot;&nbsp; Online</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        # ── Session stats ─────────────────────────────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="val">{st.session_state.total_queries}</div>'
                f'<div class="lbl">Queries</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="val">{st.session_state.total_images}</div>'
                f'<div class="lbl">Scans</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        # ── Quick prompts ─────────────────────────────────────────────────────
        st.markdown('<div class="chip-label">Quick Prompts</div>', unsafe_allow_html=True)
        for qp in QUICK_PROMPTS:
            if st.button(qp, key=f"qp_{qp}", use_container_width=True):
                state.set_quick_prompt(qp)

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        # ── Model info ────────────────────────────────────────────────────────
        with st.expander("Model Info"):
            st.caption(f"**Model:** {MODEL_NAME}")
            st.caption(f"**Temperature:** {TEMPERATURE}")
            st.caption(f"**Max tokens:** {MAX_OUTPUT_TOKENS:,}")
            st.caption("**Vision:** Enabled")

        # ── Clear button ──────────────────────────────────────────────────────
        if st.button("Clear Conversation", use_container_width=True):
            result["clear_clicked"] = True

        # ── Disclaimer ────────────────────────────────────────────────────────
        st.markdown("""
        <div class="disclaimer">
            For educational use only. Not a substitute for professional medical advice.
        </div>
        """, unsafe_allow_html=True)

    return result
