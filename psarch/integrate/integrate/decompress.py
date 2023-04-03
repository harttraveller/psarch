import zstandard

def decompress_zst(path: str) -> str:
    """
    Takes in a path to a zst file and returns the decompressed string.
    """
    with open(path, "rb") as f:
        dctx = zstandard.ZstdDecompressor()
        stream_reader = dctx.stream_reader(f)
        return stream_reader.read().decode("utf-8")
    
    
