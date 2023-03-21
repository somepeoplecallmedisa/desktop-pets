from typing import Sequence

import pygame

from src.common import Position


class Animation:
    def __init__(
        self,
        frames: Sequence[pygame.Surface],
        speed: float,
    ):
        self.frames = frames
        self.speed = speed

        self.f_len = len(self.frames)

        self.index = 0
        self.animated_once = False

    def update(self, dt: float):
        self.index += self.speed * dt

        if self.index >= self.f_len:
            self.index = 0
            self.animated_once = True

    def draw(self, screen: pygame.Surface, pos: Position):
        frame = self.frames[int(self.index)]

        screen.blit(frame, pos)

    def play(self, screen: pygame.Surface, pos: Position, dt: float):
        self.update(dt)
        self.draw(screen, pos)
