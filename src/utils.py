import pygame

from src.animation import Animation


def reverse_animation(anim: Animation):
    """Reverse frames in a given Animation"""

    new_frames = [pygame.transform.flip(frame, True, False) for frame in anim.frames]

    return Animation(new_frames, anim.speed)
