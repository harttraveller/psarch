def decompress_zst(
    path: Union[str, Path], chunk_size: int = int(2**14), max_window_size=int(2**31)
):
    decomp = ZstdDecompressor(max_window_size=max_window_size)
    with open(path, "rb") as file:
        reader = decomp.stream_reader(file)
        buffer = ""
        while True:
            chunk = reader.read(chunk_size).decode()
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line
            buffer = lines[-1]
