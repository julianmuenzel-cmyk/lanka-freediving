#!/usr/bin/env python3
"""Generate Lanka studio export packs."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MEMES = ROOT / "assets" / "studio" / "memes"
PHOTOS = ROOT / "assets" / "photos"
EXPORTS = ROOT / "assets" / "studio" / "exports"
FONT_PATH = ROOT / "assets" / "fonts" / "BowlbyOneSC-Regular.ttf"

RED = "#D94F2A"
YELLOW = "#F0C419"
CREAM = "#F5EDE0"
INK = "#1A1A1A"
TURQ = "#2BC4C4"
COBALT = "#2B3FC4"

FEED_W, FEED_H = 1080, 1440
STORY_W, STORY_H = 1080, 1920

COURSES = [
    {
        "slug": "discover",
        "name": "Discover Freediving",
        "meta": "No certification · Half day · €120",
        "copy": "Breathing and relaxation fundamentals, a shallow-water breath-hold session, safety basics. For snorkellers, surfers, and the curious.",
        "photo": "session-open.jpg",
        "bg": YELLOW,
        "fg": RED,
        "caption": "45 rpm",
    },
    {
        "slug": "wave1",
        "name": "Wave 1",
        "meta": "Molchanovs Wave 1 · 3 days · €350",
        "copy": "Online theory, pool work, static and dynamic apnea, Frenzel equalization, open water to 12–20 m.",
        "photo": "julian-line.jpg",
        "bg": YELLOW,
        "fg": RED,
        "caption": "33 rpm",
    },
    {
        "slug": "wave2",
        "name": "Wave 2",
        "meta": "Molchanovs Wave 2 · 4 days · €450",
        "copy": "Mouthfill equalization, free immersion, rescue skills, depth to 24–30 m. For certified freedivers going deeper.",
        "photo": "session-line.jpg",
        "bg": TURQ,
        "fg": COBALT,
        "caption": "78 rpm",
    },
]


def cover_crop(img: Image.Image, tw: int, th: int) -> Image.Image:
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def contain_on_canvas(img: Image.Image, tw: int, th: int, bg: str) -> Image.Image:
    canvas = Image.new("RGB", (tw, th), bg)
    sw, sh = img.size
    scale = min(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    canvas.paste(resized, ((tw - nw) // 2, (th - nh) // 2))
    return canvas


def fit_font(draw, text, max_w, start_size, font_path, min_size=14):
    size = start_size
    while size >= min_size:
        font = ImageFont.truetype(str(font_path), size)
        if draw.textlength(text, font=font) <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(str(font_path), min_size)


def wrap_text(draw, text, x, y, max_w, font, fill, line_gap=1.15):
    words = text.split()
    line = ""
    bbox = draw.textbbox((0, 0), "Ay", font=font)
    lh = int((bbox[3] - bbox[1]) * line_gap)
    cy = y
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font) > max_w and line:
            draw.text((x, cy), line, fill=fill, font=font)
            line = word
            cy += lh
        else:
            line = test
    if line:
        draw.text((x, cy), line, fill=fill, font=font)
        cy += lh
    return cy


def paste_rgba(base: Image.Image, overlay: Image.Image, xy: Tuple[int, int]):
    if overlay.mode != "RGBA":
        base.paste(overlay, xy)
        return
    base.paste(overlay, xy, overlay)


def draw_course_tile(course: dict) -> Image.Image:
    img = Image.new("RGB", (FEED_W, FEED_H), course["bg"])
    draw = ImageDraw.Draw(img)
    border = 16

    draw.rectangle([0, 0, FEED_W - 1, FEED_H - 1], outline=course["fg"], width=border)

    label_font = ImageFont.truetype(str(FONT_PATH), 42)
    draw.text((border + 8, border + 8), "COURSES", fill=course["fg"], font=label_font)

    art_h = int(FEED_H * 0.42)
    art_w = FEED_W - border * 2
    art_x = border
    art_y = border + 72
    draw.rectangle([art_x, art_y, art_x + art_w, art_y + art_h], outline=course["fg"], width=border)

    photo_path = PHOTOS / course["photo"]
    if photo_path.exists():
        photo = cover_crop(Image.open(photo_path).convert("RGB"), art_w - border * 2, art_h - border * 2)
        img.paste(photo, (art_x + border, art_y + border))

    text_x = border + 12
    text_w = FEED_W - border * 2 - 24
    y = art_y + art_h + 36

    name_font = fit_font(draw, course["name"].upper(), text_w, 92, FONT_PATH)
    draw.text((text_x, y), course["name"].upper(), fill=course["fg"], font=name_font)
    y += int(FEED_W * 0.11)

    meta_font = fit_font(draw, course["meta"].upper(), text_w, 44, FONT_PATH, 28)
    draw.text((text_x, y), course["meta"].upper(), fill=course["fg"], font=meta_font)
    y += int(FEED_W * 0.075)

    body_font = ImageFont.truetype(str(FONT_PATH), 30)
    wrap_text(draw, course["copy"], text_x, y, text_w, body_font, course["fg"])

    cap_font = ImageFont.truetype(str(FONT_PATH), 36)
    draw.text((text_x, FEED_H - border - 52), course["caption"], fill=course["fg"], font=cap_font)

    return img


def draw_opening_text(base: Image.Image, logos: Optional[Tuple[Image.Image, Image.Image]] = None) -> Image.Image:
    img = base.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    bar_h = int(h * 0.36)
    draw.rectangle([0, h - bar_h, w, h], fill=CREAM)
    draw.rectangle([0, h - bar_h, w, h - bar_h + 14], fill=RED)

    if logos:
        logo_red, logo_blue = logos
        logo_h = int(bar_h * 0.62)
        pad = int(w * 0.04)
        for logo, side in ((logo_red, "left"), (logo_blue, "right")):
            ratio = logo_h / logo.height
            logo_w = int(logo.width * ratio)
            resized = logo.resize((logo_w, logo_h), Image.LANCZOS)
            x = pad if side == "left" else w - pad - logo_w
            paste_rgba(img, resized, (x, h - bar_h + int(bar_h * 0.18)))

    max_text_w = int(w * 0.52) if logos else w - int(w * 0.14)
    y = h - bar_h + int(bar_h * 0.12)
    lines = ["LANKA FREEDIVING", "OPENING", "NOVEMBER 2026"]
    sizes = [0.09, 0.07, 0.07]
    colors = [RED, INK, RED]

    for line, ratio, color in zip(lines, sizes, colors):
        font = fit_font(draw, line, max_text_w, int(w * ratio), FONT_PATH)
        tw = draw.textlength(line, font=font)
        draw.text(((w - tw) // 2, y), line, fill=color, font=font)
        y += int(w * 0.095)

    return img


def export_grid_row(tiles: list, prefix: str):
    cols = len(tiles)
    master = Image.new("RGB", (FEED_W * cols, FEED_H))
    for i, tile in enumerate(tiles):
        master.paste(tile, (i * FEED_W, 0))
    master.save(EXPORTS / f"{prefix}-master.png", optimize=True)
    total = len(tiles)
    for visual in range(total):
        upload_num = total - visual
        tile = master.crop((visual * FEED_W, 0, (visual + 1) * FEED_W, FEED_H))
        tile.save(EXPORTS / f"{prefix}-post-{upload_num:02d}.png", optimize=True)


def make_course_grid():
    tiles = [draw_course_tile(c) for c in COURSES]
    for course, tile in zip(COURSES, tiles):
        tile.save(EXPORTS / f"lanka-course-{course['slug']}-3x4.png", optimize=True)
    export_grid_row(tiles, "lanka-course-grid")


def make_opening_grid():
    """3-post row: red logo | sunset | blue logo (place on profile grid)."""
    from generate_logo_posts import render_logo_frame, LOGO_VARIANTS

    sunset = Image.open(MEMES / "01-sunset.png").convert("RGB")
    center = draw_opening_text(cover_crop(sunset, FEED_W, FEED_H))

    logo_red = Image.open(MEMES / "logo-red.png").convert("RGBA")
    logo_blue = Image.open(MEMES / "logo-blue.png").convert("RGBA")
    left = render_logo_frame(LOGO_VARIANTS[0], logo_red, 0.0)
    right = render_logo_frame(LOGO_VARIANTS[1], logo_blue, 0.0)

    tiles = [left, center, right]
    export_grid_row(tiles, "lanka-opening-grid")


def make_scary_grid():
    src = Image.open(MEMES / "02-not-scary-wide.png").convert("RGB")
    master_w = FEED_W * 3
    framed = contain_on_canvas(src, master_w, FEED_H, YELLOW)
    framed.save(EXPORTS / "lanka-scary-grid-master.png", optimize=True)
    for visual in range(3):
        upload_num = 3 - visual
        tile = framed.crop((visual * FEED_W, 0, (visual + 1) * FEED_W, FEED_H))
        tile.save(EXPORTS / f"lanka-scary-grid-post-{upload_num:02d}.png", optimize=True)


def make_spongebob_grid():
    src = Image.open(MEMES / "07-spongebob-20m.png").convert("RGB")
    master_w = FEED_W * 3
    framed = contain_on_canvas(src, master_w, FEED_H, YELLOW)
    framed.save(EXPORTS / "lanka-spongebob-grid-master.png", optimize=True)
    for visual in range(3):
        upload_num = 3 - visual
        tile = framed.crop((visual * FEED_W, 0, (visual + 1) * FEED_W, FEED_H))
        tile.save(EXPORTS / f"lanka-spongebob-grid-post-{upload_num:02d}.png", optimize=True)


def make_opening_posts():
    sunset = Image.open(MEMES / "01-sunset.png").convert("RGB")
    feed = draw_opening_text(cover_crop(sunset, FEED_W, FEED_H))
    feed.save(EXPORTS / "lanka-opening-sunset-feed-3x4.png", optimize=True)
    story = draw_opening_text(cover_crop(sunset, STORY_W, STORY_H))
    story.save(EXPORTS / "lanka-opening-sunset-story-9x16.png", optimize=True)


def make_meme_grid():
    names = [
        "01-sunset.png",
        "02-not-scary.png",
        "03-yes-freediver.png",
        "04-conditions-beach.png",
        "05-conditions-shell.png",
        "06-cant-talk.png",
    ]
    tiles = []
    for name in names:
        src = Image.open(MEMES / name).convert("RGB")
        if name == "01-sunset.png":
            tile = draw_opening_text(cover_crop(src, FEED_W, FEED_H))
        else:
            tile = cover_crop(src, FEED_W, FEED_H)
        tiles.append(tile)

    cols, rows = 3, 2
    master = Image.new("RGB", (FEED_W * cols, FEED_H * rows))
    for i, tile in enumerate(tiles):
        master.paste(tile, ((i % cols) * FEED_W, (i // cols) * FEED_H))
    master.save(EXPORTS / "lanka-meme-grid-master.png", optimize=True)

    total = cols * rows
    for visual in range(total):
        upload_num = total - visual
        col = visual % cols
        row = visual // cols
        tile = master.crop((col * FEED_W, row * FEED_H, (col + 1) * FEED_W, (row + 1) * FEED_H))
        tile.save(EXPORTS / f"lanka-meme-grid-post-{upload_num:02d}.png", optimize=True)


def main():
    EXPORTS.mkdir(parents=True, exist_ok=True)
    make_opening_posts()
    make_opening_grid()
    make_course_grid()
    make_scary_grid()
    make_spongebob_grid()
    make_meme_grid()
    print(f"Wrote exports to {EXPORTS}")


if __name__ == "__main__":
    main()
