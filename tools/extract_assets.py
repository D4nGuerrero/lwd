"""Extract the reusable art supplied with the Laredo mockup.

The three original JPEGs are kept outside this project by Codex. Run this
script from the project directory if the attachments are still present.
"""

from pathlib import Path
from PIL import Image
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = next((ROOT / ".codex-remote-attachments").glob("*/*/1-34837.jpg")).parent
RIVER_SOURCE = next((ROOT / ".codex-remote-attachments").glob("*/*/1-34870.png"))
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

# The replacement river has its own alpha channel. Crop away the bridge while
# leaving every remaining pixel and its transparency unchanged.
river = Image.open(RIVER_SOURCE)
if river.size != (948, 1659) or river.mode != "RGBA":
    raise ValueError(f"Unexpected replacement illustration: {RIVER_SOURCE}")
river.crop((0, 600, river.width, river.height)).save(ASSETS / "river-journey.png")

print("Extracted supplied bridge, footer, river, logo and three portfolio images.")
