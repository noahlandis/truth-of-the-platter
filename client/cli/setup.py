from setuptools import setup, find_packages

# Function to read requirements.txt
def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='true-reviews-cli',
    version='0.1.0',
    packages=find_packages(where='cli'),  # Limit to cli directory
    package_dir={'': 'cli'},  # Root directory for the package
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'truereviews=cli:run_cli',  # Assuming run_cli is in cli/main.py
        ],
    },
    author='Noah Landis',
    author_email='noahlandis980@example.com',
    description='A CLI tool to aggregate restaurant reviews',
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
