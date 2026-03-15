"""
aayush/image_utils.py
──────────────────────
PIL-based image preprocessing pipeline for medical scans.
"""

import io
from PIL import Image, ImageEnhance, ImageFilter

from aayush.config import (
    MAX_IMAGE_PX,
    CONTRAST_FACTOR,
    UNSHARP_RADIUS,
    UNSHARP_PERCENT,
    UNSHARP_THRESHOLD,
)


def preprocess_image(uploaded_file) -> Image.Image:
    """
    Load an uploaded file and apply the medical-image preprocessing pipeline:
      1. Convert to RGB  (handles grayscale, RGBA, palette modes)
      2. Resize          (preserve aspect ratio, cap longest side at MAX_IMAGE_PX)
      3. Unsharp mask    (enhance edge detail for radiological features)
      4. Contrast boost  (mild enhancement for better AI interpretation)

    Returns a PIL Image object.
    """
    img = Image.open(uploaded_file)

    # 1. Normalise colour mode
    if img.mode != "RGB":
        img = img.convert("RGB")

    # 2. Resize while preserving aspect ratio
    w, h = img.size
    if max(w, h) > MAX_IMAGE_PX:
        scale = MAX_IMAGE_PX / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # 3. Sharpen edges (helps model pick up fine radiological details)
    img = img.filter(
        ImageFilter.UnsharpMask(
            radius=UNSHARP_RADIUS,
            percent=UNSHARP_PERCENT,
            threshold=UNSHARP_THRESHOLD,
        )
    )

    # 4. Mild contrast boost
    img = ImageEnhance.Contrast(img).enhance(CONTRAST_FACTOR)

    return img


def pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    """Serialise a PIL Image to raw bytes (default PNG for lossless quality)."""
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()
