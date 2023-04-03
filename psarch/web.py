from psarch.utils import detect_device_information, validate_device_information


def download_elasticsearch():
    device = detect_device_information()
    validate_device_information(device)
