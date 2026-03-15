"""
tests/test_aayush.py
---------------------
Functional test suite for the AAYUSH application.

Tests:
  1. Module imports
  2. Configuration / API key loading
  3. PIL image preprocessing pipeline
  4. Gemini API connection (live text query)
  5. Gemini API multimodal call (synthetic image + text)

Run with:
    python tests/test_aayush.py
"""

import sys
import os
import io
import traceback

# Make sure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PASS = "PASS"
FAIL = "FAIL"
results = []


def run(name, fn):
    try:
        fn()
        results.append((PASS, name, ""))
        print(f"  [ PASS ]  {name}")
    except Exception as exc:
        results.append((FAIL, name, str(exc)))
        print(f"  [ FAIL ]  {name}")
        print(f"            {exc}")


# ---------------------------------------------------------------------------
# Test 1: Module imports
# ---------------------------------------------------------------------------
def test_imports():
    from aayush.config         import GOOGLE_API_KEY, MODEL_NAME
    from aayush.image_utils    import preprocess_image, pil_to_bytes
    from aayush.gemini_client  import generate_response, get_model
    from aayush.state          import init_state
    assert MODEL_NAME, "MODEL_NAME is empty"


# ---------------------------------------------------------------------------
# Test 2: Config — API key loaded
# ---------------------------------------------------------------------------
def test_api_key_loaded():
    from aayush.config import GOOGLE_API_KEY
    assert GOOGLE_API_KEY, (
        "GOOGLE_API_KEY is empty. Make sure .env or .env.example contains the key."
    )
    assert len(GOOGLE_API_KEY) > 20, "API key looks too short to be valid"
    print(f"            Key starts with: {GOOGLE_API_KEY[:8]}...")


# ---------------------------------------------------------------------------
# Test 3: PIL preprocessing on a synthetic image
# ---------------------------------------------------------------------------
def test_image_preprocessing():
    from PIL import Image
    from aayush.image_utils import preprocess_image, pil_to_bytes

    # Create a synthetic 2000x1500 RGBA image (like a medical scan export)
    synthetic = Image.new("RGBA", (2000, 1500), color=(200, 200, 200, 255))
    buf = io.BytesIO()
    synthetic.save(buf, format="PNG")
    buf.seek(0)

    result = preprocess_image(buf)

    # Verify RGB conversion
    assert result.mode == "RGB", f"Expected RGB, got {result.mode}"
    # Verify resize: longest side must be <= 1024
    assert max(result.size) <= 1024, f"Image too large after resize: {result.size}"
    # Verify bytes conversion
    raw = pil_to_bytes(result)
    assert len(raw) > 0, "pil_to_bytes returned empty bytes"
    print(f"            Resized to {result.size[0]} x {result.size[1]} px, {len(raw):,} bytes")


# ---------------------------------------------------------------------------
# Test 4: Live Gemini API — text-only query
# ---------------------------------------------------------------------------
def test_gemini_text_response():
    from aayush.gemini_client import generate_response

    messages = []   # empty history (fresh session)
    parts    = ["Reply with exactly three words: Medical AI works"]

    response = generate_response(messages, parts)
    assert response and len(response.strip()) > 0, "Got empty response from Gemini"
    print(f"            Model replied: {response.strip()[:120]}")


# ---------------------------------------------------------------------------
# Test 5: Live Gemini API — multimodal (synthetic image + text)
# ---------------------------------------------------------------------------
def test_gemini_multimodal_response():
    from PIL import Image
    from aayush.image_utils import pil_to_bytes
    from aayush.gemini_client import generate_response

    # 256x256 greyscale synthetic "X-ray"
    synthetic = Image.new("RGB", (256, 256), color=(30, 30, 30))
    img_bytes = pil_to_bytes(synthetic)

    messages = []
    parts = [
        {"mime_type": "image/png", "data": img_bytes},
        "This is a test image. In one sentence, confirm you can see an image.",
    ]

    response = generate_response(messages, parts)
    assert response and len(response.strip()) > 0, "Got empty multimodal response from Gemini"
    print(f"            Model replied: {response.strip()[:120]}")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  AAYUSH  --  Functional Test Suite")
    print("=" * 60 + "\n")

    run("Module imports",               test_imports)
    run("API key loaded from .env",     test_api_key_loaded)
    run("PIL preprocessing pipeline",  test_image_preprocessing)
    run("Gemini API  -- text query",    test_gemini_text_response)
    run("Gemini API  -- multimodal",    test_gemini_multimodal_response)

    print("\n" + "-" * 60)
    passed = sum(1 for r in results if r[0] == PASS)
    failed = sum(1 for r in results if r[0] == FAIL)
    print(f"  Results:  {passed} passed  |  {failed} failed  |  {len(results)} total")
    print("-" * 60 + "\n")

    if failed:
        sys.exit(1)
