from setuptools import setup

setup(
    name='rgb565-converter',
    version='1.1.1',
    description='Convert a file from png to rgb565 (cpp) and vice versa.',
    url='https://github.com/CommanderRedYT/rgb565-converter',
    author='CommanderRedYT',
    license='GPLv3',
    packages=['rgb565_converter'],
    entry_points={
        'console_scripts': [
            'rgb565-converter=rgb565_converter.converter:main',
        ],
    },
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'argparse~=1.4.0',
        'Pillow~=8.1.0',
    ],
)