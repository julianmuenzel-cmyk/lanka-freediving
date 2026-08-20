#!/usr/bin/env python3
"""Generate standalone logo posts (static PNG + animated MP4)."""

from __future__ import annotations

import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
MEMES = ROOT / "assets" / "studio" / "memes"
EXPORTS = ROOT / "assets" / "studio" / "exports"
FRAMES_DIR = EXPORTS / "_logo_frames"

FEED_W, FEED_H = 1080, 1440
FPS = 30
DURATION = 4.0

RED = "#D94F2A"
YELLOW = "#F0C419"
CREAM = "#F5EDE0"
INK = "#1A1A1A"
TURQ = "#2BC4C4"
COBALT = "#2B3FC4"

LOGO_VARIANTS = [
    {
        "slug": "red",
        "logo": "logo-red.png",
        "bg": YELLOW,
        "fg": RED,
        "accent": CREAM,
    },
    {
        "slug": "blue",
        "logo": "logo-blue.png",
        "bg": TURQ,
        "fg": COBALT,
        "accent": CREAM,
    },
]

MOTIFS = [
    {"kind": "dots", "x": 0.12, "y": 0.18, "size": 0.09, "phase": 0.0},
    {"kind": "sun", "x": 0.86, "y": 0.22, "size": 0.11, "phase": 1.4},
    {"kind": "spiral", "x": 0.14, "y": 0.72, "size": 0.1, "phase": 2.8},
    {"kind": "dots", "x": 0.82, "y": 0.68, "size": 0.08, "phase": 4.2},
]


def paste_rgba(base: Image.Image, overlay: Image.Image, xy: tuple[int, int]):
    if overlay.mode != "RGBA":
        base.paste(overlay, xy)
        return
    base.paste(overlay, xy, overlay)


def draw_wave_band(draw: ImageDraw.ImageDraw, w: int, h: int, fg: str, accent: str, phase: float):
    band_top = int(h * 0.86)
    draw.rectangle([0, band_top, w, h], fill=accent)
    draw.rectangle([0, band_top, w, band_top + 14], fill=fg)

    y_base = band_top + int(h * 0.045)
    amp = h * 0.022
    step = 28
    points = []
    for x in range(-step, w + step * 2, step):
        t = (x / w) * math.tau * 2 + phase
        y = y_base + math.sin(t) * amp + math.sin(t * 1.7 + 0.6) * amp * 0.45
        points.append((x, y))
    points.extend([(w + step, h), (-step, h)])
    draw.polygon(points, fill=fg)


def draw_motif(draw: ImageDraw.ImageDraw, kind: str, cx: float, cy: float, size: float, fg: str, t: float, phase: float):
    w = FEED_W
    x = cx * w + math.sin(t * 1.3 + phase) * w * 0.018
    y = cy * FEED_H + math.cos(t * 1.1 + phase) * FEED_H * 0.012
    s = size * w
    rot = math.sin(t * 0.9 + phase) * 0.15

    if kind == "dots":
        r = s * 0.08
        offsets = [(-0.35, -0.2), (0.1, 0.25), (0.4, -0.15), (-0.1, 0.45), (0.55, 0.35)]
        for ox, oy in offsets:
            dx = x + ox * s + math.sin(t + phase + ox) * 6
            dy = y + oy * s + math.cos(t + phase + oy) * 6
            draw.ellipse([dx - r, dy - r, dx + r, dy + r], fill=fg)
    elif kind == "sun":
        cr = s * 0.22
        draw.ellipse([x - cr, y - cr, x + cr, y + cr], outline=fg, width=max(4, int(s * 0.04)))
        for i in range(8):
            ang = rot + i * (math.tau / 8)
            x1 = x + math.cos(ang) * cr * 1.15
            y1 = y + math.sin(ang) * cr * 1.15
            x2 = x + math.cos(ang) * cr * 1.75
            y2 = y + math.sin(ang) * cr * 1.75
            draw.line([(x1, y1), (x2, y2)], fill=fg, width=max(4, int(s * 0.035)))
    elif kind == "spiral":
        steps = 24
        px, py = x, y
        for i in range(steps):
            ang = rot + i * 0.42
            rad = s * 0.08 + i * s * 0.012
            nx = x + math.cos(ang) * rad
            ny = y + math.sin(ang) * rad
            draw.line([(px, py), (nx, ny)], fill=fg, width=max(3, int(s * 0.03)))
            px, py = nx, ny


def render_logo_frame(variant: dict, logo: Image.Image, t: float) -> Image.Image:
    w, h = FEED_W, FEED_H
    img = Image.new("RGB", (w, h), variant["bg"])
    draw = ImageDraw.Draw(img)
    border = 16
    draw.rectangle([0, 0, w - 1, h - 1], outline=variant["fg"], width=border)

    for m in MOTIFS:
        draw_motif(draw, m["kind"], m["x"], m["y"], m["size"], variant["fg"], t, m["phase"])

    logo_h = int(h * 0.46)
    ratio = logo_h / logo.height
    logo_w = int(logo.width * ratio)
    resized = logo.resize((logo_w, logo_h), Image.LANCZOS)
    paste_rgba(img, resized, ((w - logo_w) // 2, int(h * 0.24)))

    draw_wave_band(draw, w, h, variant["fg"], variant["accent"], t * 2.2)
    return img


def make_static(variant: dict, logo: Image.Image):
    frame = render_logo_frame(variant, logo, t=0.0)
    frame.save(EXPORTS / f"lanka-logo-{variant['slug']}-3x4.png", optimize=True)


def make_animated(variant: dict, logo: Image.Image):
    slug = variant["slug"]
    frames_path = FRAMES_DIR / slug
    frames_path.mkdir(parents=True, exist_ok=True)

    total = int(FPS * DURATION)
    for i in range(total):
        t = i / FPS
        frame = render_logo_frame(variant, logo, t)
        frame.save(frames_path / f"frame_{i:04d}.png")

    mp4_out = EXPORTS / f"lanka-logo-{slug}-animated.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", str(frames_path / "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(mp4_out),
        ],
        check=True,
        capture_output=True,
    )

    for frame in frames_path.glob("frame_*.png"):
        frame.unlink()
    try:
        frames_path.rmdir()
    except OSError:
        pass


def main():
    EXPORTS.mkdir(parents=True, exist_ok=True)
    for variant in LOGO_VARIANTS:
        logo = Image.open(MEMES / variant["logo"]).convert("RGBA")
        make_static(variant, logo)
        make_animated(variant, logo)
        print(f"  logo {variant['slug']}: PNG + MP4")
    print(f"Done → {EXPORTS}")


if __name__ == "__main__":
    main()
