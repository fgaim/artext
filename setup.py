import setuptools

from artext import __version__


def read_readme():
    with open("README.md", "r") as fh:
        return fh.read()


setuptools.setup(
    name="artext",
    version=__version__,
    author="Fitsum Gaim",
    author_email="fitsum@geezlab.com",
    description="Probabilistic Noising of Natural Language",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/fgaim/artext",
    packages=['artext'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['artext=artext.__main__:main']
    },
)
