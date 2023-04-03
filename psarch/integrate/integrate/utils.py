import json
from pathlib import Path
from typing import Union, Iterator, Any, List, Dict
from zstandard import ZstdDecompressor, ZstdError
from msgspec import Struct
from rich.console import Console
from warnings import warn


def vprint(x: Any, verbose: bool = True):
    if verbose:
        Console().print(x)


def is_zst_file(path: Union[str, Path]):
    path = str(path)
    return path.endswith(".zst")


def decompress_zst(
    path: Union[str, Path],
    chunk_size: int = int(2**14),
    max_window_size=int(2**31),
    verbose: bool = False,
) -> Iterator[str]:
    """
    Decompresses an input ZST file into an iterator of strings.

    Args:
        path (Union[str, Path]): path to zst file.
        chunk_size (int, optional): chunk size to read in. Defaults to int(2**14).
        max_window_size (_type_, optional): max memory window size. Defaults to int(2**31).

    Yields:
        Iterator[str]: iterator of strings from zst file

    Notes:
        - ! Only tested on pushshift reddit data dumps for comments and submission
    """
    decomp = ZstdDecompressor(max_window_size=max_window_size)
    with open(path, "rb") as file:
        reader = decomp.stream_reader(file)
        buffer = ""
        while True:
            try:
                chunk = reader.read(chunk_size).decode()
            except ZstdError as exc:
                raise StopIteration()
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line
            buffer = lines[-1]


def comment_struct_to_dict(comment_struct: Struct) -> Dict:
    # ? This is code used in combination with msgspec as it is faster than
    # ? cleaner looking alternatives - see benchmarks
    output = dict()
    output["controversiality"] = comment_struct.controversiality
    output["body"] = comment_struct.body
    output["subreddit_id"] = comment_struct.subreddit_id
    output["link_id"] = comment_struct.link_id
    output["stickied"] = comment_struct.stickied
    output["subreddit"] = comment_struct.subreddit
    output["score"] = comment_struct.score
    output["ups"] = comment_struct.ups
    output["author_flair_css_class"] = comment_struct.author_flair_css_class
    output["created_utc"] = comment_struct.created_utc
    output["author_flair_text"] = comment_struct.author_flair_text
    output["author"] = comment_struct.author
    output["id"] = comment_struct.id
    output["edited"] = comment_struct.edited
    output["parent_id"] = comment_struct.parent_id
    output["gilded"] = comment_struct.gilded
    output["distinguished"] = comment_struct.distinguished
    output["retrieved_on"] = comment_struct.retrieved_on
    return output


def save_json(data: Union[List, Dict], path: Union[str, Path]) -> None:
    with open(path, "w") as file:
        json.dump(data, file)
    file.close()


def add_to_list(x: Any, li: List):
    li.append(x)
