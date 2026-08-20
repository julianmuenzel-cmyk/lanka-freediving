#!/usr/bin/env python3
"""Render ocean-call popup videos (Sleeve + Quiet) with ring shake + audio."""

from __future__ import annotations

import math
import struct
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
EXPORTS = ROOT / "assets" / "studio" / "exports"
FRAMES = EXPORTS / "_popup_frames"
FONT = ROOT / "assets" / "fonts" / "BowlbyOneSC-Regular.ttf"

RED = "#D94F2A"
YELLOW = "#F0C419"
CREAM = "#F5EDE0"
INK = "#1A1A1A"

STORY_W, STORY_H = 1080, 1920
FEED_W, FEED_H = 1080, 1440
FPS = 30
RING_CYCLE = 2.15
DURATION = RING_CYCLE * 3  # three ring bursts

RING_KEYS = [
    (0.00, 0, 0, 0),
    (0.02, -7, 2, -1.1),
    (0.04, 7, -2, 1.2),
    (0.06, -6, 1, -0.9),
    (0.08, 6, 2, 0.8),
    (0.10, -4, -1, -0.6),
    (0.12, 4, 1, 0.5),
    (0.14, -2, 0, -0.25),
    (0.16, 1, 0, 0.15),
    (0.17, 0, 0, 0),
]


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def blend(fg: str, bg: str, alpha: float) -> tuple[int, int, int]:
    fr, fg_c, fb = hex_rgb(fg)
    br, bg_c, bb = hex_rgb(bg)
    return (
        int(fr * alpha + br * (1 - alpha)),
        int(fg_c * alpha + bg_c * (1 - alpha)),
        int(fb * alpha + bb * (1 - alpha)),
    )


def ring_shake(t: float, scale: float = 2.0) -> tuple[float, float, float]:
    p = (t % RING_CYCLE) / RING_CYCLE
    if p > 0.17:
        return 0.0, 0.0, 0.0
    norm = p / 0.17
    for i in range(len(RING_KEYS) - 1):
        t0, x0, y0, r0 = RING_KEYS[i]
        t1, x1, y1, r1 = RING_KEYS[i + 1]
        if norm <= t1:
            if t1 == t0:
                frac = 0
            else:
                frac = (norm - t0) / (t1 - t0)
            x = x0 + (x1 - x0) * frac
            y = y0 + (y1 - y0) * frac
            r = r0 + (r1 - r0) * frac
            return x * scale, y * scale, r
    return 0.0, 0.0, 0.0


def fit_font(draw, text, max_w, size, min_size=12):
    while size >= min_size:
        font = ImageFont.truetype(str(FONT), size)
        if draw.textlength(text, font=font) <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(str(FONT), min_size)


def draw_btn(draw, x, y, w, h, label, fg, bg, solid=False):
    if solid:
        draw.rectangle([x, y, x + w, y + h], fill=fg)
        text_color = bg
    else:
        draw.rectangle([x, y, x + w, y + h], outline=fg, width=4)
        text_color = fg
    font = fit_font(draw, label, w - 24, 28, 18)
    tw = draw.textlength(label, font=font)
    draw.text((x + (w - tw) / 2, y + (h - 28) / 2 - 2), label, fill=text_color, font=font)


def paste_shaken(base: Image.Image, art: Image.Image, cx: int, cy: int, dx: float, dy: float, angle: float):
    art = art.convert("RGBA")
    rotated = art.rotate(angle, resample=Image.BICUBIC, expand=True)
    x = int(cx - rotated.width / 2 + dx)
    y = int(cy - rotated.height / 2 + dy)
    base.paste(rotated, (x, y), rotated)


def draw_wavy_header(draw: Image.ImageDraw.ImageDraw, card_x: int, card_y: int, card_w: int, header_h: int):
    draw.rectangle([card_x, card_y, card_x + card_w, card_y + header_h], fill=INK)
    wave_y = card_y + header_h
    points = []
    step = 48
    for i, x in enumerate(range(card_x - step, card_x + card_w + step * 2, step)):
        bump = 14 if i % 2 else 0
        points.append((x, wave_y + bump))
    points.extend([(card_x + card_w + step, wave_y + 40), (card_x - step, wave_y + 40)])
    draw.polygon(points, fill=INK)


def render_popup(variant: str, t: float, w: int, h: int) -> Image.Image:
    is_sleeve = variant == "sleeve"
    overlay = blend(RED if is_sleeve else INK, INK if is_sleeve else YELLOW, 0.38 if is_sleeve else 0.42)
    frame = Image.new("RGB", (w, h), overlay)

    card_w = int(min(w * 0.82, 850))
    card_h = int(card_w * 1.35)
    card_x = (w - card_w) // 2
    card_y = (h - card_h) // 2

    fg = RED if is_sleeve else INK
    bg = CREAM
    border = 16 if is_sleeve else 8

    card = Image.new("RGB", (card_w, card_h), bg)
    draw = ImageDraw.Draw(card)
    draw.rectangle([0, 0, card_w - 1, card_h - 1], outline=fg, width=border)

    pad = 36
    y = pad

    if is_sleeve:
        kicker_font = ImageFont.truetype(str(FONT), 22)
        draw.text((pad, y), "RING RING", fill=fg, font=kicker_font)
        y += 40
        art_path = ASSETS / "shell-phone-sleeve.png"
        art_w = int(card_w * 0.55)
    else:
        header_h = 72
        draw_wavy_header(draw, 0, 0, card_w, header_h)
        kicker_font = ImageFont.truetype(str(FONT), 24)
        draw.text((pad, 22), "RING RING", fill=CREAM, font=kicker_font)
        y = header_h + 36
        art_path = ASSETS / "shell-phone-quiet.jpg"
        art_w = card_w - pad * 2

    art = Image.open(art_path).convert("RGBA")
    ratio = art_w / art.width
    art_h = int(art.height * ratio)
    art = art.resize((art_w, art_h), Image.LANCZOS)

    if not is_sleeve:
        draw.rectangle([pad - 4, y - 4, pad + art_w + 4, y + art_h + 4], outline=INK, width=4)

    dx, dy, angle = ring_shake(t, scale=2.2)
    art_cx = pad + art_w // 2
    art_cy = y + art_h // 2
    paste_shaken(card, art, art_cx, art_cy, dx, dy, angle)
    y += art_h + 28

    title = "HEY — THE OCEAN IS CALLING"
    title_font = fit_font(draw, title, card_w - pad * 2, 52, 28)
    draw.text((pad, y), title, fill=fg, font=title_font)
    y += int(card_w * 0.11)

    pick_font = ImageFont.truetype(str(FONT), 34)
    draw.text((pad, y), "PICK UP.", fill=fg, font=pick_font)
    y += 56

    btn_w = (card_w - pad * 2 - 16) // 2
    btn_h = 56
    draw_btn(draw, pad, y, btn_w, btn_h, "CONTACT US", fg, bg, solid=True)
    draw_btn(draw, pad + btn_w + 16, y, btn_w, btn_h, "WHATSAPP", fg, bg, solid=False)

    close_size = 44
    draw.rectangle([card_w - close_size - 20, 16, card_w - 20, 16 + close_size], outline=fg, width=3)
    close_font = ImageFont.truetype(str(FONT), 28)
    draw.text((card_w - close_size - 8, 20), "×", fill=fg, font=close_font)

    frame.paste(card, (card_x, card_y))
    return frame


def write_ring_audio(path: Path, duration: float):
    rate = 44100
    n = int(rate * duration)
    burst = int(rate * 0.17 * RING_CYCLE)  # shake portion
    gap = int(rate * RING_CYCLE)

    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for i in range(n):
            pos_in_cycle = i % gap
            if pos_in_cycle > burst:
                sample = 0.0
            else:
                t = i / rate
                env = min(1.0, pos_in_cycle / (rate * 0.02), (burst - pos_in_cycle) / (rate * 0.04))
                sample = env * 0.22 * (
                    math.sin(2 * math.pi * 440 * t) + math.sin(2 * math.pi * 480 * t)
                )
            wf.writeframes(struct.pack("<h", int(max(-32767, min(32767, sample * 32767)))))


def encode_video(frames_dir: Path, out_mp4: Path, audio_wav: Path | None = None):
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%04d.png"),
    ]
    if audio_wav and audio_wav.exists():
        cmd += ["-i", str(audio_wav), "-shortest"]
    cmd += [
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
    ]
    if audio_wav and audio_wav.exists():
        cmd += ["-c:a", "aac", "-b:a", "128k"]
    cmd.append(str(out_mp4))
    subprocess.run(cmd, check=True, capture_output=True)


def make_variant(variant: str, w: int, h: int, suffix: str):
    frames_dir = FRAMES / f"{variant}-{suffix}"
    frames_dir.mkdir(parents=True, exist_ok=True)
    total = int(FPS * DURATION)

    for i in range(total):
        t = i / FPS
        frame = render_popup(variant, t, w, h)
        frame.save(frames_dir / f"frame_{i:04d}.png")

    audio = EXPORTS / f"_popup-ring-{variant}.wav"
    write_ring_audio(audio, DURATION)

    out = EXPORTS / f"lanka-popup-{variant}-{suffix}.mp4"
    encode_video(frames_dir, out, audio)

    for f in frames_dir.glob("frame_*.png"):
        f.unlink()
    try:
        frames_dir.rmdir()
    except OSError:
        pass
    audio.unlink(missing_ok=True)


def main():
    EXPORTS.mkdir(parents=True, exist_ok=True)
    for variant in ("sleeve", "quiet"):
        make_variant(variant, STORY_W, STORY_H, "story-9x16")
        make_variant(variant, FEED_W, FEED_H, "feed-3x4")
        print(f"  popup {variant}: story + feed MP4")
    print(f"Done → {EXPORTS}")


if __name__ == "__main__":
    main()
