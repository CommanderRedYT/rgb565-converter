#!/usr/bin/python3
import argparse
import os
from PIL import Image
from enum import Enum

class Mode(Enum):
    CPP = ".cpp"
    PNG = ".png"

def main():
    parser = argparse.ArgumentParser(
        description="Convert a file from one format to another."
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        dest="input_file",
        help="Input file to be converted."
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        dest="output_file",
        help="Output file to be converted."
    )
    args = parser.parse_args()

    input_basename = os.path.basename(args.input_file).rsplit('.', 1)

    mode = Mode.CPP if (input_basename[1] == 'png') else Mode.PNG

    if args.output_file is None:
        args.output_file = input_basename[0] + mode.value

    output_basename = os.path.basename(args.output_file).rsplit('.', 1)

    if len(output_basename) != 2:
        print("Error: Invalid arguments.")
        exit(1)

    if (input_basename[1] not in ['png', 'cpp']):
        print("Error: Input file must be a .png or .cpp file.")
        exit(1)

    if (output_basename[1] not in ['png', 'cpp']):
        print("Error: Output file must be a .png or .cpp file.")
        print(f"Output file: {output_basename}")
        exit(1)

    if (input_basename[1] == output_basename[1]):
        print("Error: Input and output file must be different.")
        exit(1)

    if (mode == Mode.PNG):
        convert_rgb565_to_png(args)
    else:
        convert_png_to_rgb565(args)

def convert_png_to_rgb565(args):
    name = os.path.basename(args.output_file).rsplit('.', 1)[0]
    png = Image.open(args.input_file)
    width, height = png.size

    max_line_width = min(width, 64)

    # iterate over the pixels
    image = png.getdata()
    image_content = ""
    for i, pixel in enumerate(image):
        r = (pixel[0] >> 3) & 0x1F
        g = (pixel[1] >> 2) & 0x3F
        b = (pixel[2] >> 3) & 0x1F
        rgb = r << 11 | g << 5 | b
        image_content += f"0x{rgb:04X}" + (",\n    " if (i % max_line_width == max_line_width-1) else ",")

    if image_content.endswith("\n    "):
        image_content = image_content[:-5]

    output_h_content = f"""
#pragma once

#include "icon.h"

namespace bobbyicons {{
extern const espgui::Icon<{width}, {height}> {name};
}} // namespace bobbyicons
    """.strip() + "\n"

    output_cpp_content = f"""
#include "{name}.h"

namespace bobbyicons {{
const espgui::Icon<{width}, {height}> {name}{{{{
    {image_content}
}}, "{name}"}}
}} // namespace bobbyicons
    """.strip() + "\n"

    with open(args.output_file, 'w') as output_file:
        output_file.write(output_cpp_content)

    with open(args.output_file.replace('.cpp', '.h'), 'w') as output_file:
        output_file.write(output_h_content)


def convert_rgb565_to_png(args):
    with open(args.input_file, 'r') as input_file:
        tmp = input_file.read()
        icon_size = tmp.split('espgui::Icon<')[1].split('>')[0].replace(', ', ',').split(',')
        tmp = tmp.split('{{')[1].split('}')[0].split('\n')
        input_content = ""
        for line in tmp:
            input_content += line.split('//')[0].strip()
        input_content = input_content[0:-1].replace(', ', ',').split(',')

        width = int(icon_size[0])
        height = int(icon_size[1])
        png = Image.new('RGB', (width, height))

        for i, word in enumerate(input_content):
            r = (int(word, 16) >> 11) & 0x1F
            g = (int(word, 16) >> 5) & 0x3F
            b = (int(word, 16)) & 0x1F
            png.putpixel((i % width, i // width), (r << 3, g << 2, b << 3))

        png.save(args.output_file)

if __name__ == '__main__':
    main()