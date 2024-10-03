#!/usr/bin/env python3

import argparse
import os
from typing import Tuple

from PIL import Image
from enum import Enum

def hex2rgb(value: str) -> Tuple[int, int, int]:
    # value is "#5c5c5c" for example
    value = value.lstrip('#')
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

class Mode(Enum):
    CPP = ".cpp"
    PNG = ".png"

DEFAULT_CPP_TEMPLATE="""
#include "{name}.h"

namespace {namespace} {{
const espgui::Icon<{width}, {height}> {name}{{{{
    {image_content}
}}, "{name}"}};
}} // namespace {namespace}
"""

DEFAULT_H_TEMPLATE="""
#pragma once

// 3rdparty lib includes
#include <icon.h>

namespace {namespace} {{
extern const espgui::Icon<{width}, {height}> {name};
}} // namespace {namespace}
"""

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
    parser.add_argument(
        "-s",
        "--swap",
        dest="swap",
        help="Swap bytes for 16-bit words.",
        default=False,
        type=bool
    )
    parser.add_argument(
        "-n",
        "--namespace",
        dest="namespace",
        help="C++ Namespace prefix for output files.",
        default="icons",
        type=str
    )
    parser.add_argument(
        "--cpp-template-file",
        dest="cpp_template_file",
        help="C++ template file for output files.",
        default=None,
        type=str
    )
    parser.add_argument(
        "--h-template-file",
        dest="h_template_file",
        help="Header template file for output files.",
        default=None,
        type=str
    )
    parser.add_argument(
        "--background",
        dest="background",
        help="Replace transparency with a background color.",
        default=None,
        type=str
    )
    args = parser.parse_args()

    h_template = DEFAULT_H_TEMPLATE
    cpp_template = DEFAULT_CPP_TEMPLATE

    if args.cpp_template_file is not None:
        try:
            with open(args.cpp_template_file, 'r') as f:
                cpp_template = f.read()
        except:
            print("Error: Invalid C++ template file.")
            exit(1)

    if args.h_template_file is not None:
        try:
            with open(args.h_template_file, 'r') as f:
                h_template = f.read()
        except:
            print("Error: Invalid header template file.")
            exit(1)

    input_basename = os.path.basename(args.input_file).rsplit('.', 1)

    mode = Mode.CPP if (input_basename[1] == 'png') else Mode.PNG

    if args.output_file is None:
        args.output_file = input_basename[0] + mode.value

    output_basename = os.path.basename(args.output_file).rsplit('.', 1)

    if len(output_basename) != 2:
        print("Error: Invalid arguments.")
        exit(1)

    if input_basename[1] not in ['png', 'cpp']:
        print("Error: Input file must be a .png or .cpp file.")
        exit(1)

    if output_basename[1] not in ['png', 'cpp']:
        print("Error: Output file must be a .png or .cpp file.")
        print(f"Output file: {output_basename}")
        exit(1)

    if input_basename[1] == output_basename[1]:
        print("Error: Input and output file must be different.")
        exit(1)

    if mode == Mode.PNG:
        convert_rgb565_to_png(args.input_file, args.output_file, args.swap)
    else:
        convert_png_to_rgb565(args.input_file, args.output_file, args.swap, args.namespace, args.background, cpp_template, h_template)

def convert_png_to_rgb565(input_file: str, output_file: str, swap: bool, namespace: str, background: str | None, cpp_template: str = DEFAULT_CPP_TEMPLATE, h_template: str = DEFAULT_H_TEMPLATE):
    name = os.path.basename(output_file).rsplit('.', 1)[0]
    png = Image.open(input_file)
    width, height = png.size

    max_line_width = min(width, 64)

    image_content = ""
    for y in range(height):
        for x in range(width):
            pixel = png.getpixel((x, y))
            if background is not None and pixel[3] == 0:
                pixel = hex2rgb(background)
            r = (pixel[0] >> 3) & 0x1F
            g = (pixel[1] >> 2) & 0x3F
            b = (pixel[2] >> 3) & 0x1F
            rgb = r << 11 | g << 5 | b

            if swap:
                rgb = ((rgb & 0xFF) << 8) | ((rgb & 0xFF00) >> 8)
            
            image_content += f"0x{rgb:04X}" + (",\n    " if (x % max_line_width == max_line_width-1) else ",")

    if image_content.endswith("\n    "):
        image_content = image_content[:-5]

    output_h_content = h_template.format(namespace=namespace, width=width, height=height, name=name).strip() + "\n"

    output_cpp_content = cpp_template.format(namespace=namespace, width=width, height=height, name=name, image_content=image_content).strip() + "\n"
    

    with open(output_file, 'w') as f:
        f.write(output_cpp_content)

    with open(output_file.replace('.cpp', '.h'), 'w') as f:
        f.write(output_h_content)


def convert_rgb565_to_png(input_file: str, output_file: str, swap: bool):
    with open(input_file, 'r') as f:
        tmp = f.read()
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

        png.save(output_file)

if __name__ == '__main__':
    main()
