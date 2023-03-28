from zstandard import ZstdDecompressor


class ZSTIO:
    def __init__(self, file: str, chunk_size: int = 16384) -> None:
        self.fh = open(file, "rb")
        self.chunk_size = chunk_size
        self.dctx = ZstdDecompressor(max_window_size=int(2**31))
        self.reader = self.dctx.stream_reader(self.fh)
        self.buffer = ""

    def readlines(self):
        while True:
            chunk = self.reader.read(self.chunk_size).decode()
            if not chunk:
                break
            lines = (self.buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line
            self.buffer = lines[-1]
