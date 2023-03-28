from __future__ import annotations

import orjson
from zstandard import ZstdDecompressor


class ZSTJSONL:
    def __init__(
        self, path: str, chunk_size: int = int(2**20), max_window_size=int(2**31)
    ) -> None:
        # ! bug (hypothesis): if chunk size is less than the length of a line, bug introduced
        # ! and cannot read
        self.reader = ZstdDecompressor(max_window_size=max_window_size).stream_reader(
            open(path, "rb")
        )
        self.chunk_size = chunk_size
        self.buffer = ""
        self.init = self.__read_chunk()

    def __read_chunk(self) -> bool:
        # * ignoring errors seems to fix bug, but may drop bytes, bug:
        # ! UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf0 in position 1023: unexpected end of data
        self.chunk = self.reader.read(self.chunk_size).decode(errors="ignore")
        if self.chunk:
            self.lines = (self.buffer + self.chunk).split("\n")
            self.buffer = self.lines[-1]
            self.lines = self.lines[:-1]
            return True
        else:
            return False

    def __iter__(self) -> ZSTJSONL:
        return self

    def __next__(self) -> dict:
        if len(self.lines):
            return orjson.loads(self.lines.pop(0))
        else:
            if self.__read_chunk():
                return orjson.loads(self.lines.pop(0))
            else:
                raise StopIteration()
