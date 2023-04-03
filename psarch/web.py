import requests
from pathlib import Path
from psarch.term import vprint, create_progress
from psarch.utils import detect_device_information, validate_device_information


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


def download_elasticsearch():
    device = detect_device_information()
    validate_device_information(device)
