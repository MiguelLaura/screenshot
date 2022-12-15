from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="screenshot",
    version="0.1.0",
    description="A python tool to take screenshots of web pages from list of urls.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/MiguelLaura/screenshot",
    license="MIT",
    author="Laura Miguel",
    author_email="miguellaura240@gmail.com",
    keywords="screenshot",
    python_requires=">=3.6",
    packages=find_packages(exclude=["test"]),
    package_data={"docs": ["README.md"]},
    install_requires=[
        "casanova>=0.19.2,<0.20",
        "colorama>=0.4.0",
        "playwright>=1.27",
        "tqdm>=4.60.0",
    ],
    zip_safe=True,
)