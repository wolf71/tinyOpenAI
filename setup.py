import setuptools

with open('Readme.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'tinyOpenAI',
    version = '0.13',
    author = 'Charles Lai',
    author_email = '',
    description = 'Tiny OpenAI ChatGPT and Whisper API Library',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/wolf71/tinyOpenAI',
    packages = ['tinyOpenAI'],   #setuptools.find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'tinyOpenAI = tinyOpenAI:QueryDemo'
        ],
    },
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)