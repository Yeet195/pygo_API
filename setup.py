from setuptools import setup, find_packages

setup(
    name='pygo',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "requests>=2.0"
    ],
    description='A simple tool to utilize the YGOProDeck API as a Python module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Yeet195/pygo',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
