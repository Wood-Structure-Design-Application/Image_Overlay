from setuptools import setup, find_packages

setup(
    name='image_overlay',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for overlaying images based on detected points',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
    ],
)
