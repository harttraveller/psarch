import os
from pathlib import Path
from msgspec import Struct, DecodeError
from msgspec.json import decode
from typing import Optional, Any, Union, List
from rich.progress import track
from psing.object import Operation, Comment
from psing.utils import is_zst_file, decompress_zst, vprint
from psing.utils import comment_struct_to_dict
from warnings import warn
from time import perf_counter


class Reader:
    def __init__(self, path: Union[str, Path], verbose: bool = False) -> None:
        self.__path = path
        self.__verbose = verbose
        self.__operations = None

    @property
    def operations(self):
        return self.__operations

    def __filter_path(self, path: Union[str, Path]) -> List[str]:
        files = list()
        for f in os.listdir(path):
            if is_zst_file(f):
                files.append(f"{path}/{f}")
        return files

    def __parse_message(self, object: Struct) -> Optional[Any]:
        for oper in self.__operations:
            object = oper.function(object, **oper.params)
        return object

    def __handle_message(self, object: Any) -> None:
        self.__handler.function(object, **self.__handler.params)

    def add_operations(self, operations: List[Operation]) -> None:
        assert [isinstance(i, Operation) for i in operations]
        self.__operations = operations

    def add_handler(self, handler: Operation) -> None:
        assert isinstance(handler, Operation)
        self.__handler = handler

    def run(self, n_files: int, max_objects: int = 100_000_000) -> None:
        # TODO: add start and end datetime filtering
        assert self.__operations is not None
        files = self.__filter_path(self.__path)
        count = 0
        for fp in files[:n_files]:
            vprint(f"[bold blue]Starting[/bold blue]: {fp}")
            generator_object = decompress_zst(fp)
            while True:
                try:
                    data = self.__parse_message(next(generator_object))
                    self.__handle_message(data)
                    count += 1
                except:
                    break
                if count == max_objects:
                    vprint(f"[bold yellow]Hit Maximum Objects[/bold yellow]")
                    return None
            vprint(f"[bold green]Complete!")


if __name__ == "__main__":
    output = list()
    operations = [
        Operation(function=decode, params={"type": Comment}),
        Operation(function=comment_struct_to_dict),
    ]
    handler = Operation(function=output.append)
    reader = Reader("/Volumes/data/comments", verbose=False)
    # reader.add_operations(operations)
    reader.add_operations([Operation(function=lambda x: x)])
    reader.add_handler(handler)
    start = perf_counter()
    reader.run(12)
    end = perf_counter()
    n = len(output)
    vprint(f"[yellow]Parse Speed:[/yellow] {round(n / (end - start))} / second")
    print(len(set(output)))
