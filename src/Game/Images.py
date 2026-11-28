'''
This code if fully ai made since this part relies on random libraries that I don't feel like learning. The rest of the project is fully human though.
'''
'''
from io import BytesIO
from pathlib import Path
import random
from icoextract import IconExtractor
from PIL import Image



def pil_to_surface(pil_img: Image.Image) -> pygame.Surface:
    rgba = pil_img.convert("RGBA")
    buf = BytesIO()
    rgba.save(buf, format="PNG")
    buf.seek(0)
    return pygame.image.load(buf, "icon.png").convert_alpha()


def load_desktop_surfaces() -> list[tuple[str, pygame.Surface]]:
    desktop = Path.home() / "Desktop"
    temp_dir = Path("_extracted_icons")
    temp_dir.mkdir(exist_ok=True)

    image_exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".ico"}
    surfaces: list[tuple[str, pygame.Surface]] = []

    if not desktop.exists():
        return surfaces

    for item in desktop.iterdir():
        kind = "DIR " if item.is_dir() else "FILE"
        print(f"{kind}: {item.name}")

        if not item.is_file():
            continue

        suffix = item.suffix.lower()

        if suffix == ".exe":
            out_ico = temp_dir / f"{item.stem}.ico"
            try:
                extractor = IconExtractor(str(item))
                extractor.export_icon(str(out_ico))
                with Image.open(out_ico) as pil_img:
                    surface = pil_to_surface(pil_img)
                surfaces.append((item.name, surface))
            except Exception as exc:
                print(f"Skipping icon for {item.name}: {exc}")

        elif suffix in image_exts:
            try:
                surface = pygame.image.load(str(item)).convert_alpha()
                surfaces.append((item.name, surface))
            except Exception as exc:
                print(f"Skipping image {item.name}: {exc}")

    return surfaces


desktop_surfaces = load_desktop_surfaces()
print(f"Loaded {len(desktop_surfaces)} surfaces from Desktop.")
def get_random_surface_from_desktop() -> pygame.Surface | None:
    if not desktop_surfaces:
        return None
    surface = random.choice(desktop_surfaces)[1]
    pixel_resized = pygame.transform.scale(surface, (tile_size, tile_size)).convert_alpha()
    return pixel_resized
'''

import pygame
xwidth = (pygame.display.get_desktop_sizes())[0]
delta_size = xwidth
def gfos(fraction):  
    #get fraction of screen
    return delta_size / 1

images = {
    "falling_from_the_sky": pygame.transform.scale(pygame.image.load("falling_from_sky.png"), (gfos(10), gfos(10))).convert_alpha(),
    "File_explorer": pygame.transform.scale(pygame.image.load("File_Explorer_Icon.webp"), (gfos(10), gfos(10))).convert_alpha(),
    "idle": pygame.transform.scale(pygame.image.load("idle.png"), (gfos(10), gfos(10))).convert_alpha(),
    "moon": pygame.transform.scale(pygame.image.load("moon.png"), (gfos(10), gfos(10))).convert_alpha(),
    "ray": pygame.transform.scale(pygame.image.load("ray.png"), (gfos(10), gfos(10))).convert_alpha(),
    "sun": pygame.transform.scale(pygame.image.load("sun.png"), (gfos(10), gfos(10))).convert_alpha(),
    "zone_cutoff": pygame.transform.scale(pygame.image.load("zone_cutoff.png"), (gfos(10), gfos(10))).convert_alpha(),
    "meteor": pygame.transform.scale(pygame.image.load("meteor.jpeg"), (gfos(10), gfos(10))).convert_alpha(),
    "cable": pygame.transform.scale(pygame.image.load("cable.png"), (gfos(10), gfos(10))).convert_alpha(),
    "arch": pygame.transform.scale(pygame.image.load("arch.webp"), (164, 800)).convert_alpha(),
    "windows": pygame.transform.scale(pygame.image.load("windows.png"), (gfos(10), gfos(10))).convert_alpha(),
    "heart": pygame.transform.scale(pygame.image.load("heart.webp"), (gfos(10), gfos(10))).convert_alpha(),
    "banner": pygame.transform.scale(pygame.image.load("banner.png"), (gfos(10), gfos(10))).convert_alpha(),
    "busy": pygame.transform.scale(pygame.image.load("busy.png"), (gfos(10), gfos(10))).convert_alpha(),
    "play" : pygame.transform.scale(pygame.image.load("Play.png"), (gfos(10), gfos(10))).convert_alpha(),
}
