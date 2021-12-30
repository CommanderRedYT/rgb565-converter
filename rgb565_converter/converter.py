#!/usr/bin/python3
import argparse
import os
import tempfile

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

    if args.output_file is None:
        args.output_file = os.path.basename(args.input_file.rsplit('.', 1)[0]) + '.png'

    with open(args.input_file, 'r') as input_file:
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.rgb565') as tmp_file:
            tmp = input_file.read()
            icon_size = tmp.split('espgui::Icon<')[1].split('>')[0].replace(', ', ',').split(',')
            tmp = tmp.split('{{')[1].split('}')[0].split('\n')
            input_content = ""
            for line in tmp:
                input_content += line.split('//')[0].strip()
            input_content = input_content[0:-1].replace(', ', ',').split(',')

            for word in input_content:
                tmp_file.write(int(word, 16).to_bytes(2, 'little'))

            tmp_file.flush()

            os.system(f'convert -size {icon_size[0]}x{icon_size[1]} {tmp_file.name} {args.output_file}')

if __name__ == '__main__':
    main()