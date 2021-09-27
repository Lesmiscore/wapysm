import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wapysm",
    version="1.0.0",

    # guessed from commit author
    author="nao20010128nao",
    author_email="nao20010128@gmail.com",

    description="Pure-Python WebAssembly Interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/nao20010128nao/wapysm",
    packages=['wapysm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # no classifier for WASM: https://pypi.org/classifiers/
    ],
    python_requires='>=3.0',
)
