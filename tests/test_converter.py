import unittest

import os

from rgb565_converter.converter import convert_png_to_rgb565, convert_rgb565_to_png

TEST_DIRECTORY='tests'
TEST_INPUT_FILE=f'{TEST_DIRECTORY}/input_info.png'

TEST_OUTPUT_CPP_FILE=f'{TEST_DIRECTORY}/output_info.cpp'
TEST_OUTPUT_H_FILE=f'{TEST_DIRECTORY}/output_info.h'
TEST_OUTPUT_PNG_FILE=f'{TEST_DIRECTORY}/output_info_double.png'

TEST_INPUT_GREY_PNG_FILE=f'{TEST_DIRECTORY}/back.png'
TEST_OUTPUT_GREY_CPP_FILE=f'{TEST_DIRECTORY}/output_grey.cpp'
TEST_OUTPUT_GREY_H_FILE=f'{TEST_DIRECTORY}/output_grey.h'
TEST_OUTPUT_GREY_PNG_FILE=f'{TEST_DIRECTORY}/output_grey_double.png'
TEST_COMPARE_GREY_PNG_FILE=f'{TEST_DIRECTORY}/test_grey_back.png'

TEST_CUSTOM_CPP_TEMPLATE=f'{TEST_DIRECTORY}/custom_cpp_template.txt'
TEST_CUSTOM_H_TEMPLATE=f'{TEST_DIRECTORY}/custom_h_template.txt'

DO_TEARDOWN=True

class TestConverter(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        if not DO_TEARDOWN:
            return

        if os.path.exists(TEST_OUTPUT_CPP_FILE):
            os.remove(TEST_OUTPUT_CPP_FILE)

        if os.path.exists(TEST_OUTPUT_H_FILE):
            os.remove(TEST_OUTPUT_H_FILE)

        if os.path.exists(TEST_OUTPUT_PNG_FILE):
            os.remove(TEST_OUTPUT_PNG_FILE)

        if os.path.exists(TEST_OUTPUT_GREY_CPP_FILE):
            os.remove(TEST_OUTPUT_GREY_CPP_FILE)

        if os.path.exists(TEST_OUTPUT_GREY_H_FILE):
            os.remove(TEST_OUTPUT_GREY_H_FILE)

        if os.path.exists(TEST_OUTPUT_GREY_PNG_FILE):
            os.remove(TEST_OUTPUT_GREY_PNG_FILE)

    def test_converter(self):
        args = {
            'input_file': TEST_INPUT_FILE,
            'output_file': TEST_OUTPUT_CPP_FILE,
            'swap': False,
            'namespace': 'foobar',
            'background': None,
        }

        convert_png_to_rgb565(**args)

        # check if files
        self.assertTrue(os.path.exists(TEST_OUTPUT_CPP_FILE))
        self.assertTrue(os.path.exists(TEST_OUTPUT_H_FILE))

        # both files should include the custom namespace naming
        wanted_namespace_open = f'namespace {args["namespace"]} {{'
        wanted_namespace_close = f'// namespace {args["namespace"]}'

        cpp_open_correct = False
        cpp_close_correct = False
        h_open_correct = False
        h_close_correct = False

        with open(TEST_OUTPUT_CPP_FILE, 'r') as f:
            for line in f:
                if wanted_namespace_open in line:
                    cpp_open_correct = True
                if wanted_namespace_close in line:
                    cpp_close_correct = True

        with open(TEST_OUTPUT_H_FILE, 'r') as f:
            for line in f:
                if wanted_namespace_open in line:
                    h_open_correct = True
                if wanted_namespace_close in line:
                    h_close_correct = True

        # all of them should be True
        self.assertTrue(cpp_open_correct)
        self.assertTrue(cpp_close_correct)
        self.assertTrue(h_open_correct)
        self.assertTrue(h_close_correct)

        args = {
            'input_file': TEST_OUTPUT_CPP_FILE,
            'output_file': TEST_OUTPUT_PNG_FILE,
            'swap': False
        }

        convert_rgb565_to_png(**args)

        # check if both png files are binary equal
        with open(TEST_INPUT_FILE, 'rb') as f1, open(TEST_OUTPUT_PNG_FILE, 'rb') as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_converter_custom_template(self):
        cpp_template = None
        h_template = None

        with open(TEST_CUSTOM_CPP_TEMPLATE, 'r') as f:
            cpp_template = f.read()

        with open(TEST_CUSTOM_H_TEMPLATE, 'r') as f:
            h_template = f.read()

        self.assertIsNotNone(cpp_template)
        self.assertIsNotNone(h_template)

        args = {
            'input_file': TEST_INPUT_FILE,
            'output_file': TEST_OUTPUT_CPP_FILE,
            'swap': False,
            'namespace': 'foobar',
            'cpp_template': cpp_template,
            'h_template': h_template,
            'background': None,
        }

        convert_png_to_rgb565(**args)

        # check if files
        self.assertTrue(os.path.exists(TEST_OUTPUT_CPP_FILE))
        self.assertTrue(os.path.exists(TEST_OUTPUT_H_FILE))

        # both files should include the custom namespace naming
        wanted_namespace_open = f'namespace {args["namespace"]} {{'
        wanted_namespace_close = f'// namespace {args["namespace"]}'
        
        cpp_open_correct = False
        cpp_close_correct = False
        h_open_correct = False
        h_close_correct = False

        with open(TEST_OUTPUT_CPP_FILE, 'r') as f:
            for line in f:
                if wanted_namespace_open in line:
                    cpp_open_correct = True
                if wanted_namespace_close in line:
                    cpp_close_correct = True

        with open(TEST_OUTPUT_H_FILE, 'r') as f:
            for line in f:
                if wanted_namespace_open in line:
                    h_open_correct = True
                if wanted_namespace_close in line:
                    h_close_correct = True

        # all of them should be True
        self.assertTrue(cpp_open_correct)
        self.assertTrue(cpp_close_correct)
        self.assertTrue(h_open_correct)
        self.assertTrue(h_close_correct)

        args = {
            'input_file': TEST_OUTPUT_CPP_FILE,
            'output_file': TEST_OUTPUT_PNG_FILE,
            'swap': False
        }

        convert_rgb565_to_png(**args)

        # check if both png files are binary equal
        with open(TEST_INPUT_FILE, 'rb') as f1, open(TEST_OUTPUT_PNG_FILE, 'rb') as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_converter_with_grey_mode(self):
        args = {
            'input_file': TEST_INPUT_GREY_PNG_FILE,
            'output_file': TEST_OUTPUT_GREY_CPP_FILE,
            'swap': False,
            'namespace': 'foobar',
            'background': '#5c5c5c'
        }

        convert_png_to_rgb565(**args)

        # check if files exist
        self.assertTrue(os.path.exists(TEST_OUTPUT_GREY_CPP_FILE))
        self.assertTrue(os.path.exists(TEST_OUTPUT_GREY_H_FILE))

        # convert back to png
        args = {
            'input_file': TEST_OUTPUT_GREY_CPP_FILE,
            'output_file': TEST_OUTPUT_GREY_PNG_FILE,
            'swap': False
        }

        convert_rgb565_to_png(**args)

        # check if both png files are binary equal
        with open(TEST_COMPARE_GREY_PNG_FILE, 'rb') as f1, open(TEST_OUTPUT_GREY_PNG_FILE, 'rb') as f2:
            self.assertEqual(f1.read(), f2.read())

if __name__ == '__main__':
    unittest.main()
