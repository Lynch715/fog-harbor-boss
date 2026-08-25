from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
BACKGROUND = HERE / "模拟社团老大-海报底图-imagegen.png"
QR_CODE = HERE / "模拟社团老大-游戏二维码.png"
OUTPUT = HERE / "模拟社团老大-宣传海报.png"

FONT_SERIF = "/System/Library/Fonts/Supplemental/Songti.ttc"
FONT_SANS = "/System/Library/Fonts/STHeiti Medium.ttc"

GOLD = "#d8ae60"
PALE_GOLD = "#ead6ad"
WHITE = "#f5f0e5"
MUTED = "#d1d2ca"
RED = "#712024"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def gradient_overlay(canvas: Image.Image, top: int, bottom: int, start_alpha: int, end_alpha: int) -> None:
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    pixels = overlay.load()
    span = max(bottom - top, 1)
    for y in range(top, bottom):
        alpha = round(start_alpha + (end_alpha - start_alpha) * ((y - top) / span))
        for x in range(canvas.width):
            pixels[x, y] = (2, 8, 8, alpha)
    canvas.alpha_composite(overlay)


def centered_text(draw: ImageDraw.ImageDraw, box, text: str, text_font, fill, spacing=4) -> None:
    x0, y0, x1, y1 = box
    bounds = draw.multiline_textbbox((0, 0), text, font=text_font, spacing=spacing, align="center")
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    x = x0 + (x1 - x0 - width) / 2
    y = y0 + (y1 - y0 - height) / 2 - bounds[1]
    draw.multiline_text((x, y), text, font=text_font, fill=fill, spacing=spacing, align="center")


def main() -> None:
    canvas = Image.open(BACKGROUND).convert("RGBA")
    if canvas.size != (1024, 1536):
        canvas = canvas.resize((1024, 1536), Image.Resampling.LANCZOS)

    gradient_overlay(canvas, 0, 430, 205, 0)
    gradient_overlay(canvas, 900, 1536, 10, 142)

    panel = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    panel_draw = ImageDraw.Draw(panel)
    panel_draw.rectangle((0, 957, 1024, 1536), fill=(5, 8, 8, 58))
    panel_draw.line((65, 968, 959, 968), fill=(190, 143, 69, 210), width=2)
    canvas.alpha_composite(panel)

    draw = ImageDraw.Draw(canvas)
    serif_72 = font(FONT_SERIF, 72)
    serif_43 = font(FONT_SERIF, 43)
    sans_24 = font(FONT_SANS, 24)
    sans_23 = font(FONT_SANS, 23)
    sans_22 = font(FONT_SANS, 22)
    sans_20 = font(FONT_SANS, 20)
    sans_18 = font(FONT_SANS, 18)
    sans_16 = font(FONT_SANS, 16)
    sans_12 = font(FONT_SANS, 12)
    seal_font = font(FONT_SERIF, 28)

    draw.line((69, 55, 958, 55), fill=(205, 155, 74, 210), width=1)
    draw.rectangle((70, 79, 166, 191), fill=(83, 22, 24, 236), outline=(211, 169, 92, 255), width=2)
    draw.rectangle((64, 73, 172, 197), outline=(66, 17, 18, 170), width=7)
    centered_text(draw, (75, 83, 161, 187), "雾港\n和联胜", seal_font, "#f4e5c4", spacing=3)

    draw.text((204, 82), "HARBOR / 001 · 雾港风云", font=sans_20, fill=GOLD, stroke_width=1, stroke_fill=(0, 0, 0, 110))
    draw.text((198, 121), "模拟社团老大", font=serif_72, fill=WHITE, stroke_width=2, stroke_fill=(0, 0, 0, 180))
    draw.multiline_text(
        (204, 216),
        "父亲留下的不是王座，是一条老街、三名旧部，\n和一本没还完的账。",
        font=sans_24,
        fill="#e7e2d7",
        spacing=12,
        stroke_width=1,
        stroke_fill=(0, 0, 0, 150),
    )

    draw.rectangle((746, 316, 952, 362), fill=(5, 12, 12, 172))
    draw.rectangle((746, 316, 751, 362), fill=(139, 39, 40, 255))
    draw.text((771, 328), "架空剧情策略游戏", font=sans_16, fill=PALE_GOLD)

    draw.text((66, 1017), "接班不是结局，是第一场硬仗", font=sans_18, fill=GOLD)
    draw.multiline_text((65, 1055), "从一条老街开始，\n一步步坐上主位。", font=serif_43, fill=WHITE, spacing=10)
    draw.multiline_text(
        (66, 1185),
        "招人、抢地、谈判、血拼。\n地盘越打越大，人心却越来越难管——\n雾港只能有一个话事人。",
        font=sans_22,
        fill=MUTED,
        spacing=12,
    )

    labels = ["招人", "抢地", "血拼", "一统雾港"]
    x = 66
    for label in labels:
        width = 76 if len(label) == 2 else 126
        draw.rounded_rectangle((x, 1325, x + width, 1371), radius=5, fill=(5, 17, 16, 205), outline=(202, 161, 91, 135), width=1)
        bounds = draw.textbbox((0, 0), label, font=sans_18)
        tx = x + (width - (bounds[2] - bounds[0])) / 2
        draw.text((tx, 1336), label, font=sans_18, fill=PALE_GOLD)
        x += width + 12

    draw.rectangle((66, 1400, 591, 1457), fill=RED)
    draw.rectangle((66, 1400, 72, 1457), fill=(193, 143, 62, 255))
    draw.text((91, 1415), "扫码开局｜这一次，轮到你坐主位", font=sans_20, fill="#fff3da")

    draw.text((715, 1017), "扫码直接开玩", font=sans_23, fill="#f3e6ca")
    draw.rectangle((658, 1060, 958, 1360), fill=(255, 255, 255, 255), outline=(205, 161, 83, 255), width=3)
    qr = Image.open(QR_CODE).convert("RGBA").resize((270, 270), Image.Resampling.NEAREST)
    canvas.alpha_composite(qr, (673, 1075))
    draw.text((670, 1380), "lynch715.github.io/triad-boss-simulator/", font=sans_12, fill="#a6aaa3")

    draw.text((66, 1501), "本游戏为架空虚构作品 · 本地存档 · 无数据上传", font=sans_12, fill="#777e78")

    canvas.convert("RGB").save(OUTPUT, format="PNG", optimize=True)
    print(f"built {OUTPUT.name}: {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
