from zstandard import ZstdDecompressor


class ZSTIO:
    "source: https://github.com/pushshift/zreader"

    def __init__(
        self, file: str, chunk_size: int = int(2**10), max_window_size=int(2**31)
    ) -> None:
        self.decompressor = ZstdDecompressor(
            max_window_size=max_window_size
        ).stream_reader(open(file, "rb"))
        self.chunk_size = chunk_size
        self.buffer = ""

    def readlines(self):
        while True:
            # * ignoring errors seems to fix bug, but may drop bytes, bug:
            # ! UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf0 in position 1023: unexpected end of data
            chunk = self.decompressor.read(self.chunk_size).decode(errors="ignore")
            if not chunk:
                break
            lines = (self.buffer + chunk).split("\n")
            self.buffer = lines[-1]
            for line in lines[:-1]:
                yield line
