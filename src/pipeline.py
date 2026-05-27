from src.effects import (
    cinematic_motion, ultra_shake, golden_grade,
    glow_effect, lightning, smoke_system, particles,
    depth_blur, motion_blur, vignette
)
from config import FPS
import functools

def build_pipeline(base_clip):
    """
    تطبيق الـ effects على بعض بالترتيب.
    كل effect بياخد الكليب اللي قبله.
    """

    clip = base_clip.fl(cinematic_motion)
    clip = clip.fl(ultra_shake)
    clip = clip.fl(golden_grade)
    clip = clip.fl(glow_effect)

    # lightning محتاج الـ fps
    _lightning = functools.partial(lightning, fps=FPS)
    clip = clip.fl(_lightning)

    clip = clip.fl(smoke_system)
    clip = clip.fl(particles)
    clip = clip.fl(depth_blur)
    clip = clip.fl(motion_blur)
    clip = clip.fl(vignette)

    clip = clip.fadein(1.5).fadeout(1.5)

    return clip
