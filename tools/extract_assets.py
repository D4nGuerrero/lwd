"""Extract the reusable art supplied with the Laredo mockup.

The three original JPEGs are kept outside this project by Codex. Run this
script from the project directory if the attachments are still present.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import colorsys
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = next((ROOT / ".codex-remote-attachments").glob("*/*/1-34837.jpg")).parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

shutil.copyfile(SOURCE / "2-34847.jpg", ASSETS / "laredo-bridge.jpg")
shutil.copyfile(SOURCE / "3-34848.jpg", ASSETS / "underwater-catfish.jpg")

mockup = Image.open(SOURCE / "1-34837.jpg").convert("RGB")

# These are screenshots of the client sites shown inside the portfolio cards.
# Their lettering is part of those screenshots; card titles and links are HTML.
for name, box in {
    "work-border-brew.jpg": (269, 539, 389, 635),
    "work-rivas.jpg": (404, 537, 524, 635),
    "work-family-care.jpg": (541, 539, 662, 635),
}.items():
    mockup.crop(box).save(ASSETS / name, quality=96, subsampling=0)

# Isolate the actual LWD letterform. The tiny subtitle is rendered as text.
logo = mockup.crop((105, 38, 162, 63)).convert("RGBA")
pixels = logo.load()
for y in range(logo.height):
    for x in range(logo.width):
        r, g, b, _ = pixels[x, y]
        darkness = 255 - min(r, g, b)
        alpha = max(0, min(255, round((darkness - 18) * 2.5)))
        pixels[x, y] = (r, g, b, alpha)
logo.save(ASSETS / "lwd-logo.png")

# The water winds behind several content sections. Keep the original surface
# texture by lifting blue pixels from the composite rather than redrawing it.
water = mockup.crop((28, 286, 692, 1019)).convert("RGBA")
pixels = water.load()
tube = Image.new("L", water.size, 0)
draw = ImageDraw.Draw(tube)
draw.line(
    [(250, -8), (400, 22), (535, 52), (610, 88), (625, 140),
     (595, 179), (500, 197), (305, 203), (115, 210), (18, 251),
     (1, 309), (33, 359), (175, 377), (355, 385), (455, 409),
     (472, 463), (433, 516), (325, 547), (205, 586)],
    fill=255,
    width=104,
    joint="curve",
)
tube = tube.filter(ImageFilter.GaussianBlur(3))
tube_pixels = tube.load()
for y in range(water.height):
    for x in range(water.width):
        r, g, b, _ = pixels[x, y]
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        hue = h * 360
        # Cutout excludes blue portfolio imagery and typography.
        is_card = (237 <= x <= 644 and 238 <= y <= 392)
        is_testimonial = (280 <= x <= 647 and 596 <= y <= 720)
        if y < 85:
            score = min((s - 0.13) / 0.12, (v - 0.32) / 0.20,
                        (hue - 169) / 11, (212 - hue) / 11)
        else:
            score = min((s - 0.19) / 0.11, (v - 0.39) / 0.16,
                        (hue - 171) / 10, (206 - hue) / 10)
        alpha = max(0, min(255, round(score * 255)))
        alpha = round(alpha * tube_pixels[x, y] / 255)
        if y > 585:
            alpha = round(alpha * max(0, 1 - (y - 585) / 100))
        if is_card or is_testimonial:
            alpha = 0
        pixels[x, y] = (r, g, b, alpha)
water.save(ASSETS / "river-cutout.png")

# Small plants and rocks are recoverable from isolated parts of the mockup.
# A feathered edge lets each original detail meet the live page background.
shore = mockup.crop((28, 286, 692, 1019)).convert("RGBA")
mask = Image.new("L", shore.size, 0)
draw = ImageDraw.Draw(mask)
for box in [
    (156, 155, 283, 204), (474, 165, 665, 239),
    (-22, 349, 72, 416), (253, 383, 381, 449),
    (391, 385, 505, 442), (262, 562, 403, 592),
    (360, 559, 526, 593),
]:
    draw.ellipse(box, fill=255)
shore.putalpha(mask.filter(ImageFilter.GaussianBlur(5)))
shore.save(ASSETS / "shoreline-details.png")

print("Extracted original bridge, footer, logo, river and three portfolio images.")
