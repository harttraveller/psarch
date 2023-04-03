import threading
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
