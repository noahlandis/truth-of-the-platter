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
    author='Noah Landis',
    author_email='noahlandis980@example.com',
    description='A tool which aggregates restaurant reviews from Yelp, Tripadvisor, and Google to provide a more accurate rating',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/noahlandis/true-reviews',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)