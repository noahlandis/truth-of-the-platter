from setuptools import setup, find_packages

setup(
    name='true-reviews',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'geocoder',
    ],
    entry_points={
        'console_scripts': [
            'yourcli=your_cli_tool.cli:hello',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple CLI tool example',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-cli-tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)