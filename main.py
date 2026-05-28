import os
from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image
import numpy as np

from config import (
    WIDTH, HEIGHT, FPS, DURATION, SEED,
    IMAGE_PATH, OUTPUT_VIDEO, OUTPUT_DIR,
    PRESET, BITRATE, IS_CI
)
from src.effects import init_effects
from src.pipeline import build_pipeline

# =========================================================
print("=" * 52)
print("  🎬 HOGAN VAPE INTRO GENERATOR")
print(f"  📐 Resolution  : {WIDTH}x{HEIGHT}")
print(f"  🎞  FPS        : {FPS}")
print(f"  ⏱  Duration   : {DURATION}s")
print(f"  ⚙️  Preset     : {PRESET}")
print(f"  🤖 CI Mode     : {IS_CI}")
print("=" * 52)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── IMAGE ───────────────────────────────────────────────
print("📷 Loading image...")
img  = Image.open(IMAGE_PATH).convert("RGB")
img  = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
base = np.array(img)
base_clip = ImageClip(base).set_duration(DURATION)

# ─── EFFECTS ─────────────────────────────────────────────
print("⚙️  Precomputing effects...")
init_effects(fps=FPS, duration=DURATION, seed=SEED)

# ─── PIPELINE ────────────────────────────────────────────
print("🎞️  Building pipeline...")
final_clip = build_pipeline(base_clip)

# ─── AUDIO ───────────────────────────────────────────────
# الأولوية: music_final.wav → music.wav → music.mp3 → music.aac
AUDIO_CANDIDATES = [
    "assets/music_final.wav",
    "assets/music.wav",
    "assets/music.mp3",
    "assets/music.aac",
    "assets/music.ogg",
]

audio_loaded = False
for audio_path in AUDIO_CANDIDATES:
    if os.path.exists(audio_path):
        try:
            print(f"🎵 Loading audio: {audio_path}")
            audio = AudioFileClip(audio_path)
            # تأكد إن مدته مناسبة
            if audio.duration > DURATION:
                audio = audio.subclip(0, DURATION)
            audio      = audio.audio_fadein(1.5).audio_fadeout(1.5)
            final_clip = final_clip.set_audio(audio)
            print(f"✅ Audio loaded ({round(audio.duration, 1)}s)")
            audio_loaded = True
            break
        except Exception as e:
            print(f"⚠️  Failed to load {audio_path}: {e}")
            continue

if not audio_loaded:
    print("🔇 Rendering without audio.")

# ─── EXPORT ──────────────────────────────────────────────
print(f"🚀 Rendering → {OUTPUT_VIDEO}")

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

print("=" * 52)
print(f"  ✅ DONE!  →  {OUTPUT_VIDEO}")
print("=" * 52)
