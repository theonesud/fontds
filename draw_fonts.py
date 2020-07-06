from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tqdm import tqdm
import argparse
import os

text = 'Hamburgefonstiv.'
coords = [(0, 0), (256, 0), (512, 0), (768, 0),
          (0, 256), (256, 256), (512, 256), (768, 256),
          (0, 512), (256, 512), (512, 512), (768, 512),
          (0, 768), (256, 768), (512, 768), (768, 768)]


def draw_font(font_file):
    font = ImageFont.truetype(font_file, size=150)
    canvas_image = Image.new("RGB", (1024, 1024), 'white')

    for char, coord in zip(text, coords):
        w, h = font.getsize(char)
        h += int(h*0.2)  # adding the upper buffer
        char_img = Image.new("RGB", (256, 256), 'white')
        draw = ImageDraw.Draw(char_img)
        draw.text(((256 - w) / 2, (256 - h) / 2), char, fill="black", font=font)
        canvas_image.paste(char_img, coord)

    font_name = font_file.split('/')[-1][:-4]
    canvas_image.save(f'imgs/{font_name}.jpg')


def get_fontfiles():
    font_files = []
    for root, dirs, files in os.walk("fontfiles"):
        font_files += [f'{root}/{f}' for f in files if f.endswith('.ttf') or f.endswith('.otf')]
    return font_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates preview images from ttf/otf files')
    parser.add_argument('--f', type=str,
                        help='location of the font file', required=False)
    args = parser.parse_args()

    if args.f:
        draw_font(args.f)
    else:
        for file in tqdm(get_fontfiles()):
            draw_font(file)
