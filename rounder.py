"""
round_icons.py
--------------
Adds rounded corners to all images in a folder.
Saves rounded versions to a new subfolder called "rounded/"
so your originals are never touched.

Requirements:
    pip install Pillow

Usage:
    python round_icons.py
    python round_icons.py --folder path/to/icons --radius 15
"""

import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}


def add_rounded_corners(img: Image.Image, radius: int) -> Image.Image:
    """Return a copy of img with rounded corners (transparent outside)."""
    img = img.convert("RGBA")
    w, h = img.size

    # Create a mask with rounded corners
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (w - 1, h - 1)], radius=radius, fill=255)

    # Apply mask as alpha
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    result.paste(img, mask=mask)
    return result


def process_folder(folder: str, radius: int):
    input_dir = Path(folder)
    output_dir = input_dir / "rounded"
    output_dir.mkdir(exist_ok=True)

    files = [f for f in input_dir.iterdir() if f.suffix.lower() in SUPPORTED]

    if not files:
        print(f"No supported image files found in '{input_dir}'")
        return

    print(f"Processing {len(files)} file(s) → saving to '{output_dir}'\n")

    for f in files:
        try:
            img = Image.open(f)
            rounded = add_rounded_corners(img, radius)

            # Always save as PNG to preserve transparency
            out_path = output_dir / (f.stem + ".png")
            rounded.save(out_path, "PNG")
            print(f"  ✓ {f.name} → {out_path.name}")
        except Exception as e:
            print(f"  ✗ {f.name} — Error: {e}")

    print(f"\nDone! Rounded icons saved to: {output_dir.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add rounded corners to icons.")
    parser.add_argument(
        "--folder",
        default="icons",
        help="Path to your icons folder (default: ./icons)",
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=30,
        help="Corner radius in pixels (default: 10, try 8-15 for subtle rounding)",
    )
    args = parser.parse_args()
    process_folder(args.folder, args.radius)