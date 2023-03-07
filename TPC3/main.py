import re
from typing import Optional, TypedDict, Type
from pydantic import BaseModel


class Entry(TypedDict):

    folder: int
    date: str
    name: str
    father: Optional[str]
    mother: Optional[str]
    obs: Optional[str]


class Storage(BaseModel):

    all: list[Entry]
    by_folder: dict[int, list[Entry]]

    def dist_by_year(self):

        dist: dict[int, int] = {}

        for entry in self.all:

            if (year := int(entry["date"].split("-", 1)[0])) not in dist:
                dist[year] = 0

            dist[year] += 1

        return dist


def pack_entry(match: Optional[re.Match]) -> Entry:

    return Entry(
        folder=int(match[1]), date=match[2], name=match[3],
        father=match[4], mother=match[5], obs=match[6]
    )


def parse(file_path: str) -> Storage:

    parser_exp: str = r'(\d+)::(\d{4}\-\d{2}\-\d{2})::([\w\d\s,.]+)::([\w\d\s,.]+)?::([\w\d\s,.]+)?::([\w\d\s,.]+)?::'

    result = Storage(all=[], by_folder={})

    with open(file_path, "r") as file:
        data = file.readlines()

    for line in data:

        if match := re.match(parser_exp, line):

            entry: Entry = pack_entry(match)

            if entry["folder"] not in result.by_folder:
                result.by_folder[entry["folder"]] = []

            result.by_folder[entry["folder"]].append(entry)
            result.all.append(entry)

    return result


def main():
    data: Storage = parse("processos.txt")
    print(data.dist_by_year())


if __name__ == '__main__':
    SystemExit(main())
