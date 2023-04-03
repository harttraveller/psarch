import threading
import requests
from typing import Any
from pathlib import Path
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


def download_file(url: str, path: Path, block_size: int = 1024) -> None:
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
