import os
import tarfile
import platform
import subprocess
import requests
import threading

from pathlib import Path
from pyeio import easy
from typing import Any
from rich.progress import Progress
from rich.console import Console
from rich.progress import (
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TotalFileSizeColumn,
    TransferSpeedColumn,
)

from psarch.utils import detect_device_information, validate_device_information
from psarch.env import SUPPORTED_DEVICES, ELASTICSEARCH_VERSION, CONFIG_PATH
from psarch.env import CACHE_PATH, ELASTICSEARCH_VERSION, ELASTICSEARCH_DOWNLOAD_URLS


class ProgressPercentage(object):
    def __init__(self, progress: Progress, task: int) -> None:
        self._lock = threading.Lock()
        self._progress = progress
        self._task = task

    def __call__(self, bytes_amount: int) -> None:
        with self._lock:
            self._progress.update(self._task, advance=bytes_amount)


def create_progress(task: str, details: str) -> Progress:
    progress = Progress(
        TextColumn(f"[blue]{task}:[/blue] [green]{details}[/green]"),
        TotalFileSizeColumn(),
        SpinnerColumn(),
        TaskProgressColumn(),
        BarColumn(),
        TransferSpeedColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    )
    return progress


def vprint(x: Any, verbose: bool = True) -> None:
    if verbose:
        Console().print(x)


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


def download_file(url: str, path: Path, block_size: int = 1024) -> None:
    """
    Downloads a file located at the target URL. Displays a progress bar.

    Args:
        url (str): _description_
        path (Path): _description_
        block_size (int, optional): _description_. Defaults to 1024.
    """
    file_name = url.split("/")[-1]
    local_file = path / file_name
    progress = create_progress(task="DOWNLOAD", details=file_name)
    if not local_file.exists():
        with progress:
            resp = requests.get(url, stream=True)
            n_bytes = int(resp.headers.get("content-length", 0))
            task = progress.add_task(file_name, total=n_bytes)
            with open(local_file, "wb") as file:
                for data in resp.iter_content(block_size):
                    file.write(data)
                    progress.update(task, advance=block_size)
            file.close()
    else:
        vprint(f"[yellow]EXISTS: {local_file}[/yellow]")


def download_elasticsearch():
    device = detect_device_information()
    validate_device_information(device)
    if CACHE_PATH is None:
        raise Exception("Cache directory not yet set.")
    if not Path(CACHE_PATH).exists():
        raise Exception("Cache directory does not exist.")
    url = ELASTICSEARCH_DOWNLOAD_URLS[device["system"]["architecture"]]
    name = url.split("/")[-1]
    download_file(url, CACHE_PATH)


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
