import cv2
import numpy as np
import math
import random
from config import WIDTH, HEIGHT, SEED

rng = random.Random(SEED)

# =========================================================
# CINEMATIC CAMERA MOVEMENT
# =========================================================

def cinematic_motion(get_frame, t):
    frame = get_frame(t)
    scale = 1 + (0.025 * t)
    resized = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    h, w = resized.shape[:2]
    x = int((w - WIDTH) / 2 + math.sin(t) * 40)
    y = int((h - HEIGHT) / 2 + math.cos(t * 1.2) * 30)
    return resized[y:y+HEIGHT, x:x+WIDTH]

# =========================================================
# CINEMATIC SHAKE
# =========================================================

def ultra_shake(get_frame, t):
    frame = get_frame(t)
    dx = int(math.sin(t * 15) * 6)
    dy = int(math.cos(t * 18) * 6)
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(frame, M, (WIDTH, HEIGHT), borderMode=cv2.BORDER_REFLECT)

# =========================================================
# GOLDEN COLOR GRADE
# =========================================================

def golden_grade(get_frame, t):
    frame = get_frame(t)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.35, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.15, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

# =========================================================
# GLOW
# =========================================================

def glow_effect(get_frame, t):
    frame = get_frame(t)
    blur = cv2.GaussianBlur(frame, (0, 0), 25)
    return cv2.addWeighted(frame, 1.0, blur, 0.45, 0)

# =========================================================
# LIGHTNING FLASH - seed-based للـ consistency
# =========================================================

# احسب مسبقا امتى هيحصل flash
_flash_frames = set()
_flash_strengths = {}

def _precompute_flashes(fps, duration, seed):
    total = int(fps * duration)
    r = random.Random(seed)
    for i in range(total):
        if r.random() > 0.985:
            _flash_frames.add(i)
            _flash_strengths[i] = r.randint(50, 120)

def lightning(get_frame, t, fps=30):
    frame = get_frame(t).copy()
    frame_idx = int(t * fps)
    if frame_idx in _flash_frames:
        strength = _flash_strengths[frame_idx]
        white = np.full_like(frame, strength)
        frame = cv2.add(frame, white)
    return frame

# =========================================================
# SMOKE SYSTEM - precomputed positions
# =========================================================

_smoke_data = []

def _precompute_smoke(n=80, seed=42):
    r = random.Random(seed)
    for _ in range(n):
        _smoke_data.append({
            "x":      r.randint(0, WIDTH),
            "y":      r.randint(int(HEIGHT * 0.45), HEIGHT),
            "radius": r.randint(40, 180),
            "alpha":  r.uniform(0.02, 0.06),
            "color":  (r.randint(180, 255), r.randint(180, 255), r.randint(180, 255))
        })

def smoke_system(get_frame, t):
    frame = get_frame(t).copy()
    for s in _smoke_data:
        overlay = frame.copy()
        cv2.circle(overlay, (s["x"], s["y"]), s["radius"], s["color"], -1)
        frame = cv2.addWeighted(overlay, s["alpha"], frame, 1 - s["alpha"], 0)
    return frame

# =========================================================
# FIRE PARTICLES - precomputed
# =========================================================

_particle_data = []

def _precompute_particles(n=250, seed=99):
    r = random.Random(seed)
    for _ in range(n):
        _particle_data.append({
            "x":     r.randint(0, WIDTH),
            "y":     r.randint(0, HEIGHT),
            "size":  r.randint(1, 5),
            "color": (r.randint(180, 255), r.randint(80, 180), 0)
        })

def particles(get_frame, t):
    frame = get_frame(t).copy()
    for p in _particle_data:
        cv2.circle(frame, (p["x"], p["y"]), p["size"], p["color"], -1)
    return frame

# =========================================================
# DEPTH OF FIELD
# =========================================================

_dof_gradient = None

def _precompute_dof():
    global _dof_gradient
    g = np.linspace(0.2, 1, HEIGHT)
    g = np.tile(g, (WIDTH, 1)).T
    _dof_gradient = cv2.merge([g, g, g])

def depth_blur(get_frame, t):
    frame = get_frame(t).astype(np.float64)
    blur = cv2.GaussianBlur(frame.astype(np.uint8), (0, 0), 6).astype(np.float64)
    result = frame * _dof_gradient + blur * (1 - _dof_gradient)
    return np.clip(result, 0, 255).astype(np.uint8)

# =========================================================
# MOTION BLUR
# =========================================================

_motion_kernel = None

def _precompute_motion_blur(kernel_size=25):
    global _motion_kernel
    k = np.zeros((kernel_size, kernel_size))
    k[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
    _motion_kernel = k / kernel_size

def motion_blur(get_frame, t):
    frame = get_frame(t)
    blurred = cv2.filter2D(frame, -1, _motion_kernel)
    return cv2.addWeighted(frame, 0.85, blurred, 0.15, 0)

# =========================================================
# VIGNETTE
# =========================================================

_vignette_mask = None

def _precompute_vignette():
    global _vignette_mask
    X = cv2.getGaussianKernel(WIDTH, WIDTH / 2)
    Y = cv2.getGaussianKernel(HEIGHT, HEIGHT / 2)
    kernel = Y * X.T
    _vignette_mask = kernel / kernel.max()

def vignette(get_frame, t):
    frame = get_frame(t).astype(np.float64)
    for i in range(3):
        frame[:, :, i] *= _vignette_mask
    return np.clip(frame, 0, 255).astype(np.uint8)

# =========================================================
# INIT ALL PRECOMPUTED DATA
# =========================================================

def init_effects(fps, duration, seed=SEED):
    _precompute_flashes(fps, duration, seed)
    _precompute_smoke(seed=seed)
    _precompute_particles(seed=seed + 57)
    _precompute_dof()
    _precompute_motion_blur()
    _precompute_vignette()
    print("✅ All effects precomputed.")
