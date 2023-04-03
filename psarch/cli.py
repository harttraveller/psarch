import os
import click
import tarfile
import platform
import requests
import subprocess
from pathlib import Path
from pyeio import easy
from urllib.request import urlretrieve
from psarch.env import CONFIG, ELASTICSEARCH_DOWNLOAD_URLS
from psarch.web import download_file


def check_config():
    if not CONFIG.exists():
        easy.save({"cache": None}, CONFIG)


def make_cache(path: str):
    pass


def download_elasticsearch():
    system = platform.system()
    if system != "Darwin":
        raise Exception("Currently only supports MacOS")
    cache = Path(easy.load(CONFIG)["cache"])
    if cache is None:
        raise Exception("Cache directory not set")
    if not Path(cache).exists():
        raise Exception("Cache directory does not exist")
    architecture = platform.processor()
    if not (cache / "elasticsearch-8.7.0").exists():
        if architecture == "arm":
            download_file(ELASTICSEARCH_DOWNLOAD_URLS["macOS_aarch64"], cache)
            file = tarfile.open(cache / "elasticsearch-8.7.0-darwin-aarch64.tar.gz")
            file.extractall(cache)
            file.close()
            os.remove(cache / "elasticsearch-8.7.0-darwin-aarch64.tar.gz")
        elif architecture == "i386":
            download_file(ELASTICSEARCH_DOWNLOAD_URLS["macOS_x86_64"], cache)
            file = tarfile.open(cache / "elasticsearch-8.7.0-darwin-x86_64.tar.gz")
            file.extractall(cache)
            file.close()
            os.remove(cache / "elasticsearch-8.7.0-darwin-x86_64.tar.gz")
        else:
            raise Exception("Unsupported chipset architecture")


def start_elasticsearch():
    cache = Path(easy.load(CONFIG)["cache"])
    subprocess.run(str(Path(cache) / "elasticsearch-8.7.0" / "bin" / "elasticsearch"))


def test_elasticsearch():
    resp = requests.get("http://localhost:9200")
    if resp.status_code == 200:
        print("Working")
    else:
        print("Not working...")


def update_elasticsearch_security():
    # https://www.reddit.com/r/elasticsearch/comments/uog64y/error_when_connecting_to_elasticsearch/
    cache = easy.load(CONFIG)["cache"]
    with open(
        Path(cache) / "elasticsearch-8.7.0" / "config" / "elasticsearch.yml"
    ) as es_config_file:
        es_config = es_config_file.read()
    es_config_file.close()
    es_config = es_config + "\nxpack.security.enabled: false"
    with open(
        Path(cache) / "elasticsearch-8.7.0" / "config" / "elasticsearch.yml", "w"
    ) as es_config_file:
        es_config_file.write(es_config)
    es_config_file.close()


@click.group()
def entry():
    pass


@entry.group()
def cache():
    pass


@cache.command()
def update():
    check_config()
    print("Enter the working directory you would like to cache data in.")
    cache = str(input(">>> "))
    if Path(cache).exists():
        easy.save({"cache": cache}, CONFIG)
    else:
        print("Directory does not exist.")


@cache.command()
def view():
    check_config()
    cache = easy.load(CONFIG)["cache"]
    if cache is not None:
        print(cache)
    else:
        print("No cache directory configured.")


@cache.command()
def open():
    check_config()
    cache = easy.load(CONFIG)["cache"]
    if cache is not None:
        if Path(cache).exists():
            pass  # open folder
        else:
            print("Cache directory path invalid.")
    else:
        print("No cache directory configured.")


@entry.group()
def elastic():
    pass


@elastic.command()
def download():
    download_elasticsearch()


@elastic.command()
def test():
    test_elasticsearch()


@elastic.command()
def security():
    update_elasticsearch_security()


@elastic.command()
def start():
    start_elasticsearch()


@entry.group()
def data():
    pass


@data.command()
def download():
    pass


@entry.command()
def run():
    pass
