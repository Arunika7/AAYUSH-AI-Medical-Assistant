"""
aayush/ui/styles.py
────────────────────
Injects the custom CSS into the Streamlit page.
Call `inject_styles()` once at the top of app.py after `set_page_config`.
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root & Reset ── */
:root {
    --bg-primary:    #0a0e1a;
    --bg-secondary:  #111827;
    --bg-card:       rgba(255,255,255,0.04);
    --border:        rgba(255,255,255,0.08);
    --accent:        #3b82f6;
    --accent-glow:   rgba(59,130,246,0.35);
    --accent2:       #06b6d4;
    --success:       #10b981;
    --warning:       #f59e0b;
    --danger:        #ef4444;
    --text-primary:  #f1f5f9;
    --text-secondary:#94a3b8;
    --text-muted:    #475569;
    --radius:        16px;
    --radius-sm:     10px;
    --shadow:        0 8px 32px rgba(0,0,0,0.5);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 900px 600px at 15% 10%, rgba(59,130,246,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 700px 500px at 85% 90%, rgba(6,182,212,0.10) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stHeader"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1426 0%, #0a0e1a 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Inputs ── */
textarea, input[type="text"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.25s !important;
}
textarea:focus, input[type="text"]:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 14px var(--accent-glow) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px var(--accent-glow) !important;
    filter: brightness(1.1) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    transition: border-color 0.25s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

/* ── Chat messages ── */
.chat-row { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 18px; }
.chat-row.user { flex-direction: row-reverse; }

.avatar {
    width: 38px; height: 38px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.avatar.ai   { background: linear-gradient(135deg, var(--accent), var(--accent2)); box-shadow: 0 0 16px var(--accent-glow); }
.avatar.user { background: linear-gradient(135deg, #7c3aed, #a855f7); box-shadow: 0 0 16px rgba(124,58,237,0.4); }

.bubble {
    max-width: 78%;
    padding: 14px 18px;
    border-radius: var(--radius);
    line-height: 1.65;
    font-size: 0.92rem;
    backdrop-filter: blur(12px);
}
.bubble.ai {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.2);
    border-top-left-radius: 4px;
}
.bubble.user {
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.2);
    border-top-right-radius: 4px;
}

/* ── Chat container ── */
.chat-container {
    max-height: 58vh;
    overflow-y: auto;
    padding: 1.5rem 0.5rem;
    scroll-behavior: smooth;
}
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-track { background: transparent; }
.chat-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── Header ── */
.aayush-header {
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(6,182,212,0.10));
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}
.aayush-header::before {
    content: "";
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(59,130,246,0.18), transparent 70%);
}
.aayush-header h1 {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #60a5fa, #22d3ee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 4px 0 !important;
    letter-spacing: -0.5px;
}
.aayush-header p { color: var(--text-secondary) !important; margin: 0 !important; font-size: 0.95rem; }

/* ── Disclaimer banner ── */
.disclaimer {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: var(--radius-sm);
    padding: 10px 16px;
    font-size: 0.78rem;
    color: #fbbf24;
    margin-top: 10px;
}

/* ── Quick prompt chips ── */
.chip-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 6px;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #34d399;
}
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: #10b981; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.2rem 0;
}

/* ── Metrics row ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    text-align: center;
    backdrop-filter: blur(8px);
}
.metric-card .val { font-size: 1.4rem; font-weight: 700; color: var(--accent); }
.metric-card .lbl { font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.8px; }

/* ── Image preview ── */
.img-preview {
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    overflow: hidden;
    background: var(--bg-card);
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div { border-top-color: var(--accent) !important; }

/* scrollbar global */
* { scrollbar-width: thin; scrollbar-color: var(--border) transparent; }
</style>
"""


def inject_styles() -> None:
    """Inject all custom CSS into the current Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)
