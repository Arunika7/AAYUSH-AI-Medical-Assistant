"""
aayush/config.py
────────────────
All application-wide constants: model settings, system prompt,
quick-prompt list. Import from here to keep config in one place.
"""

import os
from dotenv import load_dotenv

load_dotenv()              # reads .env (if it exists)
load_dotenv(".env.example")  # fallback: reads .env.example


# ── API key (loaded from .env — never exposed in the UI) ──────────────────────
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# ── Model settings ─────────────────────────────────────────────────────────────
MODEL_NAME        = "gemini-2.0-flash"
TEMPERATURE       = 0.4
TOP_P             = 0.9
MAX_OUTPUT_TOKENS = 2048

# ── Image preprocessing ────────────────────────────────────────────────────────
MAX_IMAGE_PX      = 1024   # longest side after resize
CONTRAST_FACTOR   = 1.15   # mild contrast boost
UNSHARP_RADIUS    = 1
UNSHARP_PERCENT   = 120
UNSHARP_THRESHOLD = 3

# ── Safety thresholds ─────────────────────────────────────────────────────────
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
]

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are AAYUSH (Advanced AI for Your Universal Specialized Healthcare), an expert AI medical assistant.

Your capabilities:
- Analyze medical imaging: X-rays, MRI scans, CT scans, ultrasound images, and pathology slides
- Answer clinical questions with evidence-based, structured responses
- Discuss symptoms, diagnoses, treatments, medications, and medical procedures
- Provide differential diagnoses and suggest diagnostic pathways

When analyzing medical images, always structure your response as:
**Imaging Modality and View:** [Identify the type and orientation]
**Key Observations:** [Bullet each finding]
**Notable Findings:** [Highlight abnormalities if present]
**Clinical Impression:** [Summary assessment]
**Recommendations:** [Suggested next steps]

When answering clinical questions, use clear headers, bullet points, and evidence-based information.

IMPORTANT: Always append this at the end of every response:
---
*Medical Disclaimer: This analysis is AI-generated and intended for educational purposes only. It does not constitute professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.*
"""

# ── Quick-prompt shortcuts (sidebar buttons) ───────────────────────────────────
QUICK_PROMPTS = [
    "Analyse chest X-ray findings",
    "Interpret this MRI scan",
    "Describe cardiac abnormalities",
    "Identify bone fractures",
    "Explain lab results",
    "Drug interactions overview",
]

# ── Allowed image extensions ───────────────────────────────────────────────────
ALLOWED_IMAGE_TYPES = ["png", "jpg", "jpeg", "bmp", "tiff", "webp"]
