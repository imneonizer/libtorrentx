from setuptools import setup, Extension
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="libtorrentx",
    scripts=["script/libtorrentx"],
    version="0.0.3",
    description="libtorrent python api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nitin Rai",
    author_email="mneonizer@gmail.com",
    url="https://github.com/imneonizer/libtorrentx",
    license="MIT License",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["libtorrent>=2.0.6", "ujson>=5.2.0", "easydict>=1.9"],
    platforms=["linux", "unix"],
    python_requires=">3.5.2",
)
