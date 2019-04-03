import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uitestframework",
    version="0.0.1",
    author="Joshua Cruz",
    author_email="joshua.cruz15@upr.edu",
    description="A small package for UI testing in web applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Joshuacruzc/uitestframework",
    packages=setuptools.find_packages(),
    install_requires=['selenium'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
