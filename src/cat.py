import pygame

from src.animation import Animation
from src.common import EventInfo, Position
from src.enums import EntityStates
from src.utils import reverse_animation


class Cat:
    def __init__(self, assets: dict):
        self.screen_size = pygame.display.get_window_size()
        self.animations = {
            "walk_left": Animation(assets["cat_walk"], 0.05),
            "idle_left": Animation(assets["cat_idle"], 0.005),
            "jump_left": Animation(assets["cat_jump"], 1),
        }
        self.animations |= {
            "walk_right": reverse_animation(self.animations["walk_left"]),
            "idle_right": reverse_animation(self.animations["idle_left"]),
            "jump_right": reverse_animation(self.animations["jump_left"]),
        }
        self.pos = pygame.Vector2()
        self.vel = pygame.Vector2(0)
        self.gravity = 0.25
        self.rect = self.animations["jump_left"].frames[0].get_rect()

        self.state = EntityStates.WALK
        self.facing = "right"

    def move_dnd(self, event_info: EventInfo):
        """Drag-and-drop cat movement"""
        self.rect.center = event_info["mouse_pos"]
        self.pos.xy = self.rect.topleft
        self.vel.y = 0

    def move(self, dt: float):
        self.pos += self.vel * dt
        self.rect.topleft = self.pos
        self.vel.y += self.gravity * dt

        if self.vel.x > 0:
            self.facing = "right"
        elif self.vel.x < 0:
            self.facing = "left"

    def update(self, event_info: EventInfo):
        if event_info["mouse_btn"][0]:
            self.move_dnd(event_info)
        else:
            self.move(event_info["dt"])

        if self.rect.bottom >= self.screen_size[1]:
            self.vel.y = 0
            self.rect.bottom = self.screen_size[1]
            self.pos.y = self.rect.top

        if self.rect.left <= 0:
            self.vel.x *= -1
            self.rect.left = 0
            self.pos.x = self.rect.x
        elif self.rect.right >= self.screen_size[0]:
            self.vel.x *= -1
            self.rect.right = self.screen_size[0]
            self.pos.x = self.rect.x

    def draw(self, screen: pygame.Surface, event_info: EventInfo):
        self.animations[f"{self.state.value}_{self.facing}"].play(
            screen, self.pos, event_info["dt"]
        )
