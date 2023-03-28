import os
from pyeio import easy
from rich.progress import track
from psarch.io import ZSTJSONL

COMMENTS_PATH = "/Volumes/Elements/data/pushshift/reddit/comments"
SUBMISSIONS_PATH = "/Volumes/Elements/data/pushshift/reddit/submissions"
MAX_LINES_PER_FILE = 10_000


def run_counts(path: str, maxlines: int, name: str) -> None:
    files = [i for i in os.listdir(path) if i.split(".")[-1] == "zst"]
    key_counts = dict()
    n_comments = 0
    for file in track(files, description=name):
        file_path = f"{path}/{file}"
        data = ZSTJSONL(file_path)
        count = 0
        for line in data:
            for key in line.keys():
                if key in key_counts.keys():
                    key_counts[key] += 1
                else:
                    key_counts[key] = 1
            n_comments += 1
            count += 1
            if count > maxlines:
                break

    easy.save(
        {"total": n_comments, "key_counts": key_counts},
        f"../files/{name}_key_count_sample.json",
    )


if __name__ == "__main__":
    run_counts(COMMENTS_PATH, MAX_LINES_PER_FILE, "comments")
    run_counts(SUBMISSIONS_PATH, MAX_LINES_PER_FILE, "submissions")
