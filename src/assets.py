import json
from pathlib import Path
from typing import List, Sequence

import pygame


def get_images(
    sheet: pygame.Surface,
    size: Sequence[int],
) -> List[pygame.Surface]:
    """
    Converts a sprite sheet to a list of surfaces
    Parameters:
        sheet: A pygame.Surface that contains the sprite sheet
        size: Size of a sprite in the sprite sheet
    """
    images = []

    width, height = size

    # loop through all sprites in the sprite sheet
    rows = int(sheet.get_height() / height)
    columns = int(sheet.get_width() / width)

    for row in range(rows):
        for col in range(columns):
            image = sheet.subsurface(pygame.Rect((col * width), (row * height), *size))

            images.append(image)

    return images


def load_assets() -> dict:
    assets = {}
    path = Path("assets/")

    json_files = path.rglob("*.json")
    for metadata_f in json_files:
        metadata = json.loads(metadata_f.read_text())
        for file, data in metadata.items():
            complete_path = metadata_f.parent / file
            if data["convert_alpha"]:
                image = pygame.image.load(complete_path).convert_alpha()
            else:
                image = pygame.image.load(complete_path).convert()

            asset = image
            if data["resize_by"] != 1:
                image = pygame.transform.scale_by(image, data["resize_by"])

                if data["sprite_sheet"] is not None:
                    asset = get_images(
                        image, pygame.Vector2(data["sprite_sheet"]) * data["resize_by"]
                    )

            else:
                if data["sprite_sheet"] is not None:
                    asset = get_images(image, data["sprite_sheet"])

            file_extension = file[file.find(".") :]
            assets[file.replace(file_extension, "")] = asset

    return assets
