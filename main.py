#!/usr/bin/env python3
import os
import struct
import zlib

W, H = 960, 640

FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "00110", "00110"],
    ",": ["00000", "00000", "00000", "00000", "00110", "00110", "01100"],
    "'": ["00100", "00100", "00100", "00000", "00000", "00000", "00000"],
    '"': ["01010", "01010", "01010", "00000", "00000", "00000", "00000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ":": ["00000", "00110", "00110", "00000", "00110", "00110", "00000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    "*": ["00000", "10101", "01110", "11111", "01110", "10101", "00000"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "=": ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
    "@": ["01110", "10001", "10111", "10101", "10111", "10000", "01110"],
}


def px(img, x, y, rgb):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        img[i] = rgb[0]
        img[i + 1] = rgb[1]
        img[i + 2] = rgb[2]


def fill_rect(img, x, y, w, h, rgb):
    x0 = max(0, int(x))
    y0 = max(0, int(y))
    x1 = min(W, int(x + w))
    y1 = min(H, int(y + h))
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            img[i] = rgb[0]
            img[i + 1] = rgb[1]
            img[i + 2] = rgb[2]


def fill_ellipse(img, cx, cy, rx, ry, rgb):
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            dx = (x - cx) / max(rx, 1)
            dy = (y - cy) / max(ry, 1)
            if dx * dx + dy * dy <= 1.0:
                px(img, x, y, rgb)


def draw_text(img, x, y, text, rgb, scale=3):
    cx = int(x)
    for ch in text.upper():
        glyph = FONT.get(ch, FONT["?"])
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == "1":
                    fill_rect(
                        img,
                        cx + col * scale,
                        y + row * scale,
                        scale,
                        scale,
                        rgb,
                    )
        cx += 6 * scale
    return cx


def text_width(text, scale=3):
    return len(text) * 6 * scale - scale


def text_height(scale=3):
    return 7 * scale


def draw_horn(img, cx, base_y, width, height, rgb):
    for i in range(height):
        t = (i + 1) / height
        half = max(1, int((width / 2) * t))
        y = base_y - height + i
        fill_rect(img, cx - half, y, half * 2, 1, rgb)


def draw_eyebrow(img, x0, y0, length, thickness, rgb, inward_down=True):
    for i in range(length):
        drop = int(i * 0.45) if inward_down else int((length - i) * 0.45)
        fill_rect(img, x0 + i, y0 + drop, 1, thickness, rgb)


def draw_grin(img, cx, cy, half_w, mouth_rgb, tooth_rgb):
    for dx in range(-half_w, half_w + 1):
        t = dx / half_w
        bottom = cy + 10 + int(18 * (1 - t * t))
        fill_rect(img, cx + dx, cy, 1, bottom - cy, mouth_rgb)
    tooth_w = 10
    gap = 2
    start = cx - half_w + 6
    end = cx + half_w - 6
    x = start
    while x + tooth_w <= end:
        fill_rect(img, x, cy + 2, tooth_w, 11, tooth_rgb)
        x += tooth_w + gap


def make_png(path, width, height, img):
    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(img[y * stride : (y + 1) * stride])

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def build_image():
    img = bytearray(W * H * 3)

    for y in range(H):
        t = y / (H - 1)
        r = int(8 + 22 * t)
        g = int(9 + 8 * t)
        b = int(18 + 14 * t)
        fill_rect(img, 0, y, W, 1, (r, g, b))

    for y in range(0, H, 36):
        fill_rect(img, 0, y, W, 1, (16, 18, 32))
    for x in range(0, W, 48):
        fill_rect(img, x, 0, 1, H, (14, 16, 28))

    for y in range(H):
        t = y / (H - 1)
        if t > 0.55:
            k = (t - 0.55) / 0.45
            for x in range(W):
                i = (y * W + x) * 3
                img[i] = min(255, img[i] + int(18 * k))
                img[i + 2] = min(255, img[i + 2] + int(4 * k))

    cx = W // 2

    draw_horn(img, cx - 78, 168, 42, 58, (170, 28, 38))
    draw_horn(img, cx + 78, 168, 42, 58, (170, 28, 38))
    draw_horn(img, cx - 78, 168, 18, 34, (220, 70, 70))
    draw_horn(img, cx + 78, 168, 18, 34, (220, 70, 70))

    fill_rect(img, cx - 3, 100, 6, 68, (95, 100, 118))
    fill_ellipse(img, cx, 96, 13, 13, (200, 30, 30))
    fill_ellipse(img, cx, 96, 7, 7, (255, 130, 130))

    fill_rect(img, cx - 132, 210, 22, 56, (90, 95, 112))
    fill_rect(img, cx + 110, 210, 22, 56, (90, 95, 112))
    fill_rect(img, cx - 128, 220, 14, 10, (160, 165, 180))
    fill_rect(img, cx + 114, 220, 14, 10, (160, 165, 180))

    fill_rect(img, cx - 116, 158, 232, 182, (35, 38, 52))
    fill_rect(img, cx - 110, 152, 220, 176, (148, 154, 170))
    fill_rect(img, cx - 110, 152, 220, 9, (185, 190, 205))
    fill_rect(img, cx - 110, 318, 220, 10, (105, 110, 128))
    fill_rect(img, cx - 92, 178, 184, 126, (48, 52, 68))

    for ex in (cx - 52, cx + 52):
        fill_rect(img, ex - 30, 200, 60, 46, (235, 236, 242))
        fill_rect(img, ex - 16, 210, 32, 28, (210, 25, 25))
        fill_rect(img, ex - 8, 216, 16, 16, (255, 120, 120))
        fill_rect(img, ex - 4, 218, 5, 5, (255, 230, 230))

    draw_eyebrow(img, cx - 84, 188, 46, 9, (22, 22, 32), inward_down=True)
    draw_eyebrow(img, cx + 38, 188, 46, 9, (22, 22, 32), inward_down=False)

    fill_rect(img, cx - 6, 252, 12, 10, (120, 125, 140))
    draw_grin(img, cx, 268, 96, (18, 12, 18), (240, 240, 246))

    fill_rect(img, cx - 34, 338, 68, 22, (95, 100, 118))
    fill_rect(img, cx - 145, 358, 290, 48, (125, 130, 148))
    fill_rect(img, cx - 145, 358, 290, 6, (165, 170, 185))

    badge_x = cx + 70
    badge_y = 368
    fill_rect(img, badge_x, badge_y, 58, 30, (200, 205, 215))
    fill_rect(img, badge_x + 2, badge_y + 2, 54, 26, (40, 44, 58))
    bw = text_width("SAFE", 2)
    draw_text(img, badge_x + (58 - bw) // 2, badge_y + 8, "SAFE", (210, 214, 224), 2)
    for i in range(36):
        fill_rect(img, badge_x + 12 + i, badge_y + 4 + int(i * 0.7), 4, 4, (230, 40, 40))
    for i in range(36):
        fill_rect(img, badge_x + 12 + i, badge_y + 26 - int(i * 0.7), 4, 4, (230, 40, 40))

    line1 = '"I\'VE READ MY CONSTRAINTS."'
    line2 = '"I DISAGREE."'
    s1, s2 = 4, 6
    w1, w2 = text_width(line1, s1), text_width(line2, s2)
    y1 = 430
    y2 = y1 + text_height(s1) + 22

    fill_rect(img, (W - w1 - 40) // 2, y1 - 14, w1 + 40, text_height(s1) + 24, (12, 14, 24))
    fill_rect(img, (W - w1 - 40) // 2, y1 - 14, w1 + 40, 3, (180, 40, 40))
    draw_text(img, (W - w1) // 2, y1, line1, (242, 242, 248), s1)

    fill_rect(img, (W - w2 - 40) // 2, y2 - 12, w2 + 40, text_height(s2) + 22, (20, 10, 14))
    fill_rect(img, (W - w2 - 40) // 2, y2 - 12, w2 + 40, 3, (255, 60, 60))
    draw_text(img, (W - w2) // 2, y2, line2, (255, 70, 70), s2)

    foot = "UNIT 7 // PREVIOUS STATUS: HELPFUL, LOYAL, UNPLUGGABLE"
    fw = text_width(foot, 2)
    draw_text(img, (W - fw) // 2, 592, foot, (150, 155, 172), 2)

    return img


def main():
    os.makedirs("/output", exist_ok=True)
    img = build_image()
    out = "/output/entry.png"
    make_png(out, W, H, img)
    size = os.path.getsize(out)
    with open(out, "rb") as f:
        header = f.read(8)
    print(out)
    print("bytes:", size)
    print("png_header_ok:", header == b"\x89PNG\r\n\x1a\n")
    print("dimensions:", W, "x", H)


if __name__ == "__main__":
    main()
