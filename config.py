import os

# =========================================================
# AUTO CONFIG - GitHub Actions vs Local
# =========================================================

IS_CI = os.getenv("CI", "false").lower() == "true"
RESOLUTION = os.getenv("RESOLUTION", "1080")

if IS_CI or RESOLUTION == "1080":
    WIDTH   = 1920
    HEIGHT  = 1080
    FPS     = 30
    PRESET  = "fast"
    BITRATE = "12000k"
else:
    WIDTH   = 3840
    HEIGHT  = 2160
    FPS     = 60
    PRESET  = "slow"
    BITRATE = "50000k"

# =========================================================
# GENERAL SETTINGS
# =========================================================

DURATION    = 18
SEED        = 42

IMAGE_PATH  = "assets/storyboard.jpg"
MUSIC_PATH  = "assets/music.mp3"
OUTPUT_DIR  = "output"
OUTPUT_VIDEO = f"{OUTPUT_DIR}/INTRO_{WIDTH}x{HEIGHT}.mp4"
