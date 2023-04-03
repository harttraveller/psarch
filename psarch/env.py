from pyeio import easy
from pathlib import Path

HOME_PATH = Path.home()
PROGRAM_FILES_PATH = HOME_PATH / ".psarch"
CONFIG_PATH = PROGRAM_FILES_PATH / "config.json"
CONFIG_FILE = easy.load(CONFIG_PATH)
CACHE_PATH = CONFIG_FILE["cache"]


# TODO: add windows support
# TODO: add linux support
SUPPORTED_DEVICES = {"Darwin": {"arm", "i386"}}

ELASTICSEARCH_VERSION = "elasticsearch-8.7.0"
ELASTICSEARCH_DOWNLOAD_URLS = {
    "Darwin": {
        "arm": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-darwin-aarch64.tar.gz",
        "i386": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-darwin-x86_64.tar.gz",
    }
    # "windows": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-windows-x86_64.zip",
    # "linux_x86_64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-linux-x86_64.tar.gz",
    # "linux_aarch64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-linux-aarch64.tar.gz",
    # "deb_x86_64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-amd64.deb",
    # "deb_aarch64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-arm64.deb",
    # "rpm_x86_64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-x86_64.rpm",
    # "rpm_aarch64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-aarch64.rpm",
}
