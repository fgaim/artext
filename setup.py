import setuptools

from artext import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="artext",
    version=__version__,
    author="Fitsum Gaim",
    author_email="fitsum@geezlab.com",
    description="Probabilistic Noising of Natural Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fgaim/artext",
    packages=['artext'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
