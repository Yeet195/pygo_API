from setuptools import setup, find_packages

setup(
    name='pygo',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "requests>=2.0"
    ],
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_module',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
