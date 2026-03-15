"""
aayush/ui/chat.py
──────────────────
Renders the scrollable chat history panel and the hero header banner.
"""

import streamlit as st


def render_header() -> None:
    """Display the AAYUSH gradient hero header."""
    st.markdown("""
    <div class="aayush-header">
        <h1>AAYUSH</h1>
        <p>Advanced AI for Your Universal Specialized Healthcare &nbsp;&middot;&nbsp; Powered by Gemini 2.0 Flash</p>
    </div>
    """, unsafe_allow_html=True)


def render_chat_history(messages: list) -> None:
    """
    Render the full conversation history as styled chat bubbles inside a
    scrollable container.

    Args:
        messages: List of {role: str, content: str} dicts from session state.
    """
    chat_html = '<div class="chat-container">'

    if not messages:
        chat_html += """
        <div style="text-align:center; padding: 3rem 1rem; color: #475569;">
            <div style="font-size:1.1rem; font-weight:600; color:#64748b;">Welcome to AAYUSH</div>
            <div style="font-size:0.88rem; margin-top:6px;">
                Upload an X-ray, MRI, or CT scan &mdash; or ask any clinical question to begin.
            </div>
        </div>
        """
    else:
        for msg in messages:
            role     = msg["role"]
            content  = msg["content"]
            avatar   = "AI" if role == "assistant" else "You"
            row_cls  = "ai" if role == "assistant" else "user"
            chat_html += (
                f'<div class="chat-row {row_cls}">'
                f'<div class="avatar {row_cls}">{avatar}</div>'
                f'<div class="bubble {row_cls}">{content}</div>'
                f'</div>'
            )

    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
