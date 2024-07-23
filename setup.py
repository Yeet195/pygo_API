from setuptools import setup, find_packages

setup(
    name='pygo_API',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        "requests>=2.0"
    ],
    description='A simple tool to utilize the YGOProDeck API as a Python module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Yeet195/pygo_API',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
