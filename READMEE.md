# 🎬 Hogan Vape - Cinematic Intro Generator

Ultra cinematic 4K intro generator using Python + MoviePy.

## Structure

```
hogan-vape-intro/
├── .github/workflows/render.yml   ← GitHub Action
├── src/
│   ├── effects.py                 ← Visual effects
│   └── pipeline.py               ← Effects pipeline
├── assets/
│   ├── storyboard.jpg            ← Input image (not in git)
│   └── music.mp3                 ← Audio (optional, not in git)
├── output/                       ← Rendered videos (not in git)
├── main.py                       ← Entry point
├── config.py                     ← Settings
└── requirements.txt
```

## Run Locally

```bash
pip install -r requirements.txt
python main.py
```

## Run on GitHub Actions

1. Go to **Actions** tab
2. Select **🎬 Render Cinematic Intro**
3. Click **Run workflow**
4. Choose resolution: `1080` or `4K`
5. Download the result from **Artifacts**

## Notes

- 1080p@30fps → ~15-20 min render on GitHub Actions ✅
- 4K@60fps → local machine only (GPU recommended)
- Assets are excluded from git — add them manually
