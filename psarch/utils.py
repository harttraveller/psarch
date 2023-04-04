import os
import tarfile
import platform
import subprocess
import requests
from pathlib import Path
from pyeio import easy
from psarch.term import vprint
from psarch.env import SUPPORTED_DEVICES, ELASTICSEARCH_VERSION, CONFIG_PATH


def validate_device_information(device: dict[str, str]) -> None:
    """
    Throws an exception if the OS and chipset architecture are not yet supported.

    Args:
        device (dict[str, str]): _description_

    Raises:
        NotImplementedError: _description_
        NotImplementedError: _description_
    """
    if device["system"] not in SUPPORTED_DEVICES.keys():
        raise NotImplementedError("This operating system is currently unsupported.")
    if device["architecture"] not in SUPPORTED_DEVICES[device["system"]]:
        raise NotImplementedError("This chipset architecture is currently unsupported.")


def detect_device_information() -> dict[str, str]:
    """
    Detects the current device OS and chip architecture.
    Used to determine elalsticsearch version and OS-specific
    commands.

    Returns:
        dict[str, str]: A dictionary with the system (OS) and chip architecture.
    """
    system = platform.system()
    architecture = platform.processor()
    device = {"system": system, "architecture": architecture}
    return device


def unzip_tarfile(path: str) -> None:
    with tarfile.open(path) as file:
        file.extractall("/".join(path.split("/")[:-1]))
    file.close()
    os.remove(path)


def start_elasticsearch():
    subprocess.run(
        str(Path(CONFIG_PATH) / ELASTICSEARCH_VERSION / "bin" / "elasticsearch")
    )


def test_elasticsearch():
    resp = requests.get("http://localhost:9200")
    if resp.status_code == 200:
        vprint("\n[green]Elasticsearch is working[/green]")
    else:
        vprint(
            "\n[red]Elastic search is not working. Disabling security may fix this issue.[/red]"
        )
