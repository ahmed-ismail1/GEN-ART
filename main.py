from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image
import numpy as np
import os

from config import (
    WIDTH, HEIGHT, FPS, DURATION, SEED,
    IMAGE_PATH, MUSIC_PATH, OUTPUT_VIDEO, OUTPUT_DIR,
    PRESET, BITRATE, IS_CI
)
from src.effects import init_effects
from src.pipeline import build_pipeline

# =========================================================
# STARTUP INFO
# =========================================================

print("=" * 50)
print(f"🎬 HOGAN VAPE INTRO GENERATOR")
print(f"   Resolution : {WIDTH}x{HEIGHT}")
print(f"   FPS        : {FPS}")
print(f"   Duration   : {DURATION}s")
print(f"   Preset     : {PRESET}")
print(f"   CI Mode    : {IS_CI}")
print("=" * 50)

# =========================================================
# OUTPUT FOLDER
# =========================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# LOAD IMAGE
# =========================================================

print("📷 Loading image...")
img = Image.open(IMAGE_PATH).convert("RGB")
img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
base = np.array(img)
base_clip = ImageClip(base).set_duration(DURATION)

# =========================================================
# INIT EFFECTS
# =========================================================

print("⚙️  Precomputing effects...")
init_effects(fps=FPS, duration=DURATION, seed=SEED)

# =========================================================
# BUILD PIPELINE
# =========================================================

print("🎞️  Building pipeline...")
final_clip = build_pipeline(base_clip)

# =========================================================
# AUDIO
# =========================================================

try:
    audio = AudioFileClip(MUSIC_PATH)
    audio = audio.audio_fadein(1).audio_fadeout(1)
    final_clip = final_clip.set_audio(audio)
    print("🎵 Audio loaded.")
except Exception as e:
    print(f"⚠️  No audio: {e}")

# =========================================================
# EXPORT
# =========================================================

print(f"🚀 Rendering to: {OUTPUT_VIDEO}")

final_clip.write_videofile(
    OUTPUT_VIDEO,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    bitrate=BITRATE,
    preset=PRESET,
    threads=4,
    logger="bar"
)

print("=" * 50)
print("✅ DONE!")
print(f"📁 Output: {OUTPUT_VIDEO}")
print("=" * 50)
