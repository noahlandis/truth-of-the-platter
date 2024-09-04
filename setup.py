from setuptools import setup, find_packages

# Function to read requirements.txt
def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='true-reviews',
    version='1.0.0',
    packages=find_packages(),
    install_requires=read_requirements(),  # use requirements.txt
    entry_points={
        'console_scripts': [
            'truereviews=src.main:main',
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
