import os
from pyeio import easy
from rich.progress import track
from psarch.io import ZSTJSONL

COMMENTS_PATH = "/Volumes/Elements/data/pushshift/reddit/comments"
SUBMISSIONS_PATH = "/Volumes/Elements/data/pushshift/reddit/submissions"
MAX_LINES_PER_FILE = 10_000


def run_collection(path: str, maxlines: int, name: str) -> None:
    files = [i for i in os.listdir(path) if i.split(".")[-1] == "zst"]
    examples = dict()
    for file in track(files, description=name):
        file_path = f"{path}/{file}"
        data = ZSTJSONL(file_path)
        count = 0
        for line in data:
            for key, value in line.items():
                if key in examples.keys():
                    if len(examples[key]) < 10:
                        if value not in examples[key]:
                            examples[key].append(value)
                else:
                    examples[key] = [value]
            count += 1
            if count >= maxlines:
                break
    easy.save(
        examples,
        f"../files/{name}_example_sample.json",
    )


if __name__ == "__main__":
    run_collection(COMMENTS_PATH, MAX_LINES_PER_FILE, "comments")
    run_collection(SUBMISSIONS_PATH, MAX_LINES_PER_FILE, "submissions")
