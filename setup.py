# flake8: noqa
import os
import setuptools


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name = "comfyui-api",
    version = "2.0.0",
    description = "Asynchronous-capable API for ComfyUI",
    long_description = read('README.md'),
    url = "https://github.com/DeInfernal/comfyui_api.git",
    packages = setuptools.find_packages(),
    install_requires=["aiohttp"],
    author = "'6'",
    license = "Free",
    keywords = "API ComfyUI"
)
