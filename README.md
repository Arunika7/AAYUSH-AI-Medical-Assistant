# AAYUSH — AI-Powered Medical Assistant

**Advanced AI for Your Universal Specialized Healthcare**

A multimodal medical chatbot that analyses medical images (X-rays, MRI, CT scans) and answers clinical queries using Google Gemini 2.0 Flash. Built with Python, Streamlit, and PIL.

---

## Features

- **Multimodal Analysis** — Upload X-rays, MRIs, CT scans, ultrasound images or pathology slides and receive structured radiological interpretations
- **Clinical Q&A** — Evidence-based answers to pharmacology, pathology, and general clinical questions
- **Image Preprocessing** — PIL pipeline: auto-resize to 1024 px, RGB normalisation, unsharp-mask sharpening, and contrast enhancement before sending to the model
- **Persistent Chat History** — Full conversation memory within a session with a scrollable bubble interface
- **Quick Prompts** — One-click sidebar shortcuts for common clinical queries
- **Auto Retry** — Exponential backoff on API rate-limit errors (5 s, 15 s, 30 s)
- **Dark UI** — Glassmorphism cards, gradient header, custom scrollbar, powered by vanilla CSS with no frontend framework

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Frontend | Streamlit |
| AI Model | Google Gemini 2.0 Flash (multimodal) |
| Image Processing | Pillow (PIL) |
| Environment | python-dotenv |

---

## Project Structure

```
Aayush/
├── app.py                        # Entry point — wires all modules together
├── requirements.txt              # Python dependencies
├── .env.example                  # API key template (copy to .env)
├── .gitignore
├── README.md
└── aayush/                       # Core Python package
    ├── __init__.py
    ├── config.py                 # All constants: model name, system prompt, quick-prompts
    ├── image_utils.py            # PIL preprocessing pipeline
    ├── gemini_client.py          # Gemini API: model init, history, response with retry
    ├── state.py                  # Streamlit session-state init and helpers
    └── ui/                       # UI sub-package
        ├── __init__.py
        ├── styles.py             # Custom CSS (injected via inject_styles())
        ├── sidebar.py            # Sidebar: stats, quick prompts, model info
        ├── chat.py               # Header and chat bubble renderer
        └── input_panel.py        # File upload + text query area
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A [Google AI Studio](https://aistudio.google.com/app/apikey) API key (free tier available)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/aayush.git
cd aayush

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
copy .env.example .env
# Open .env and replace the placeholder with your real key:
# GOOGLE_API_KEY=AIza...
```

### Run

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## Usage

### Text Query
1. Type a clinical question in the **Your Question** text area
2. Click **Send to AAYUSH**
3. The assistant returns a structured, evidence-based response with a medical disclaimer

### Image Analysis
1. Upload a medical image (PNG, JPG, JPEG, BMP, TIFF, or WEBP) in the **Upload Medical Image** panel
2. Optionally add a specific question, or leave blank for a full radiological analysis
3. Click **Send to AAYUSH**

### Quick Prompts
Click any button in the sidebar to pre-fill the query box with a common clinical request:
- Analyse chest X-ray findings
- Interpret this MRI scan
- Describe cardiac abnormalities
- Identify bone fractures
- Explain lab results
- Drug interactions overview

---

## Configuration

All tunable parameters are in `aayush/config.py`:

| Parameter | Default | Description |
|---|---|---|
| `MODEL_NAME` | `gemini-2.0-flash` | Gemini model identifier |
| `TEMPERATURE` | `0.4` | Response creativity (0 = deterministic) |
| `MAX_OUTPUT_TOKENS` | `2048` | Maximum response length |
| `MAX_IMAGE_PX` | `1024` | Max image dimension after resize |
| `CONTRAST_FACTOR` | `1.15` | PIL contrast enhancement multiplier |

---

## Security Notes

- Your API key is loaded from `.env` at startup and is **never** shown in the UI
- `.env` is excluded from version control via `.gitignore`
- Commit only `.env.example` (which contains a placeholder, not a real key)

---

## Disclaimer

AAYUSH is intended for **educational and research purposes only**. The AI-generated responses do not constitute professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical decisions.

---

## License

MIT License — see [LICENSE](LICENSE) for details.