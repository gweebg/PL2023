import os

from typing import Callable

from TPC1.models import Entry
from TPC1.storage import Storage


def read_csv(file_path: str, validator: Callable[[list[str]], bool]) -> Storage:

    csv_entries: Storage = Storage()

    if not os.path.isfile(file_path):
        raise Exception(f"{file_path} is not an existing file.")

    with open(file_path, "r") as csv_file:
        lines: list[str] = csv_file.readlines()

    lines.pop(0)
    for csv_line in lines:

        parsed_line: list[str] = csv_line.split(",")

        if validator(parsed_line):
            csv_entries.add(Entry.from_line(parsed_line))

    csv_entries.finish()

    return csv_entries




