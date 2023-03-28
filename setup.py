import atexit
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install


def post_install():
    package_files = Path.home() / ".psarch"
    package_files.mkdir(exist_ok=True)


class Installation(install):
    def __init__(self, *args, **kwargs):
        super(Installation, self).__init__(*args, **kwargs)
        atexit.register(post_install)


setup(
    name="psarch",
    version="0.0.0",
    author="Hart Traveller",
    url="https://github.com/harttraveller/psarch",
    license="MIT",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["msgspec"],
    entry_points={"console_scripts": ["psarch=psarch.cli:entry"]},
    cmdclass={
        "install": Installation,
    },
)
