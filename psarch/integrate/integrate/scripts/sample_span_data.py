import os
from pyeio import easy
from rich.progress import track
from psarch.io import ZSTJSONL

COMMENTS_PATH = "/Volumes/Elements/data/pushshift/reddit/comments"
SUBMISSIONS_PATH = "/Volumes/Elements/data/pushshift/reddit/submissions"
MAX_LINES_PER_FILE = 1_000


def run_collection(path: str, maxlines: int, name: str) -> None:
    files = [i for i in os.listdir(path) if i.split(".")[-1] == "zst"]
    output = list()
    for file in track(files, description=name):
        file_path = f"{path}/{file}"
        data = ZSTJSONL(file_path)
        for _ in range(maxlines):
            try:
                output.append(next(data))
            except:
                break
    easy.save(
        output,
        f"../files/{name}_sample.json",
    )


if __name__ == "__main__":
    run_collection(COMMENTS_PATH, MAX_LINES_PER_FILE, "comments")
    run_collection(SUBMISSIONS_PATH, MAX_LINES_PER_FILE, "submissions")
