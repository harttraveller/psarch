import os
import tarfile
import platform
from psarch.env import SUPPORTED_DEVICES


def validate_device_information(device: dict[str, str]) -> None:
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
