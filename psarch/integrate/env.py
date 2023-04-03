from pathlib import Path

HOME = Path.home()
FILES = HOME / ".psarch"
CONFIG = FILES / "config.json"


ELASTICSEARCH_DOWNLOAD_URLS = {
    # "windows": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-windows-x86_64.zip",
    "macOS_x86_64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-darwin-x86_64.tar.gz",
    "macOS_aarch64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-darwin-aarch64.tar.gz",
    # "linux_x86_64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-linux-x86_64.tar.gz",
    # "linux_aarch64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-linux-aarch64.tar.gz",
    # "deb_x86_64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-amd64.deb",
    # "deb_aarch64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-arm64.deb",
    # "rpm_x86_64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-x86_64.rpm",
    # "rpm_aarch64": "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-aarch64.rpm",
}
