import pygame
import win32api
import win32con
import win32gui

from src.assets import load_assets
from src.cat import Cat
from src.common import EventInfo

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
SIZE = pygame.display.get_window_size()
clock = pygame.time.Clock()

win32gui.SetWindowPos(
    pygame.display.get_wm_info()["window"],
    win32con.HWND_TOPMOST,
    0,
    0,
    0,
    0,
    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
)
fuchsia = (255, 0, 128)  # Transparency color
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(
    hwnd,
    win32con.GWL_EXSTYLE,
    win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(
    hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY
)

assets = load_assets()
cat = Cat(assets)

mouse_pos_last = pygame.Vector2(0, 0)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    mouse_pos = pygame.mouse.get_pos()
    mouse_vel = mouse_pos - mouse_pos_last
    mouse_pos_last = pygame.Vector2(mouse_pos)

    event_info: EventInfo = {
        "dt": clock.tick(60) / 10,
        "mouse_btn": pygame.mouse.get_pressed(),
        "mouse_pos": mouse_pos,
        "mouse_vel": mouse_vel,
    }

    screen.fill(fuchsia)

    cat.update(event_info)
    cat.draw(screen, event_info)

    pygame.display.flip()
