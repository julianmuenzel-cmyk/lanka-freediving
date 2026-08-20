#!/usr/bin/env python3
"""Add animated Lanka text overlay to source video."""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "assets" / "studio" / "exports"
FRAMES = EXPORTS / "_video_overlay_frames"
FONT = ROOT / "assets" / "fonts" / "BowlbyOneSC-Regular.ttf"

RED = "#D94F2A"
YELLOW = "#F0C419"
CREAM = "#F5EDE0"
INK = "#1A1A1A"

SEQUENCE = [
    {"text": "LANKA FREEDIVING", "start": 0.0, "end": 4.0},
    {"text": "OPENING IN NOVEMBER", "start": 4.0, "end": 8.0},
    {"text": "SOUTH COAST SRI LANKA", "start": 8.0, "end": None},
]

FADE = 0.35


def probe_video(path: Path) -> tuple[int, int, float, float]:
    import json

    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
            "-show_entries", "format=duration",
            "-of", "json",
            str(path),
        ],
        text=True,
    )
    data = json.loads(out)
    stream = data["streams"][0]
    w, h = int(stream["width"]), int(stream["height"])
    duration = float(data["format"]["duration"])
    rate = stream["r_frame_rate"]
    num, den = rate.split("/")
    fps = float(num) / float(den)
    return w, h, duration, fps


def active_line(t: float, duration: float) -> tuple[str | None, float]:
    for item in SEQUENCE:
        end = duration if item["end"] is None else item["end"]
        if t < item["start"] or t >= end:
            continue
        fade_in = min(1.0, max(0.0, (t - item["start"]) / FADE))
        fade_out = 1.0
        if item["end"] is not None:
            fade_out = min(1.0, max(0.0, (item["end"] - t) / FADE))
        return item["text"], fade_in * fade_out
    return None, 0.0


def fit_font(draw, text, max_w, size, min_size=24):
    while size >= min_size:
        font = ImageFont.truetype(str(FONT), size)
        if draw.textlength(text, font=font) <= max_w:
            return font
        size -= 4
    return ImageFont.truetype(str(FONT), min_size)


def draw_overlay(w: int, h: int, text: str, alpha: float) -> Image.Image:
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if alpha <= 0:
        return overlay

    draw = ImageDraw.Draw(overlay)
    scale = w / 1080
    border = int(16 * scale)
    pad_x = int(48 * scale)
    pad_y = int(36 * scale)
    max_text_w = int(w * 0.86)

    font = fit_font(draw, text, max_text_w - pad_x * 2, int(72 * scale), int(28 * scale))
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    box_w = int(tw + pad_x * 2)
    box_h = int(th + pad_y * 2 + border * 2)
    box_x = (w - box_w) // 2
    box_y = int(h * 0.68) - box_h // 2

    a = int(255 * alpha)
    cream = (*ImageColor_to_rgb(CREAM), a)
    red = (*ImageColor_to_rgb(RED), a)
    yellow = (*ImageColor_to_rgb(YELLOW), a)
    ink = (*ImageColor_to_rgb(INK), a)

    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill=cream, outline=red, width=border)
    rule_h = max(6, int(10 * scale))
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + rule_h], fill=red)

    text_x = box_x + (box_w - tw) // 2
    text_y = box_y + rule_h + pad_y // 2
    draw.text((text_x, text_y), text, fill=(red[0], red[1], red[2], a), font=font)

    dot_r = max(4, int(6 * scale))
    for dx, dy, col in [
        (box_x + int(24 * scale), box_y + box_h - int(28 * scale), yellow),
        (box_x + box_w - int(24 * scale), box_y + box_h - int(28 * scale), yellow),
    ]:
        draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=(col[0], col[1], col[2], a))

    return overlay


def ImageColor_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def render_overlay_frames(w: int, h: int, duration: float, fps: float):
    """Render overlay at 1080×1920 then upscale — much faster at 4K source."""
    ow, oh = 1080, 1920
    FRAMES.mkdir(parents=True, exist_ok=True)
    total = int(math.ceil(duration * fps))
    for i in range(total):
        if i % 60 == 0:
            print(f"  overlay frame {i}/{total}", flush=True)
        t = i / fps
        text, alpha = active_line(t, duration)
        frame = draw_overlay(ow, oh, text, alpha) if text else Image.new("RGBA", (ow, oh), (0, 0, 0, 0))
        if w != ow or h != oh:
            frame = frame.resize((w, h), Image.LANCZOS)
        frame.save(FRAMES / f"overlay_{i:04d}.png", optimize=True)
    return total


def compose(source: Path, output: Path, fps: float, total: int):
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(source),
            "-framerate", str(fps),
            "-i", str(FRAMES / "overlay_%04d.png"),
            "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p",
            "-frames:v", str(total),
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "fast",
            "-c:a", "copy",
            "-movflags", "+faststart",
            str(output),
        ],
        check=True,
        capture_output=True,
    )


def cleanup(total: int):
    for i in range(total):
        p = FRAMES / f"overlay_{i:04d}.png"
        p.unlink(missing_ok=True)
    try:
        FRAMES.rmdir()
    except OSError:
        pass


def main():
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "/Users/jules/Downloads/ProjectEditData_787266058.165444_22091765573631.MP4"
    )
    if not source.exists():
        print(f"Missing source: {source}", file=sys.stderr)
        sys.exit(1)

    EXPORTS.mkdir(parents=True, exist_ok=True)
    output = EXPORTS / "lanka-spongebob-opening-overlay.mp4"

    w, h, duration, fps = probe_video(source)
    print(f"Source {w}x{h} · {duration:.1f}s · {fps:.2f}fps")

    total = render_overlay_frames(w, h, duration, fps)
    compose(source, output, fps, total)
    cleanup(total)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
