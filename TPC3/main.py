import re
import json

from typing import Optional, TypedDict
from pydantic import BaseModel
from collections import Counter


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

    def dist_by_names(self) -> dict[str, dict[int, list[str]]]:

        result: dict[str, dict[int, list[str]]] = {
            "names": {},
            "surnames": {}
        }

        for entry in self.all:

            entry_century: int = get_century(int(entry["date"].split("-", 1)[0]))

            if entry_century not in result["names"] or entry_century not in result["surnames"]:
                result["names"][entry_century] = []
                result["surnames"][entry_century] = []

            split_name: list[str] = entry["name"].split(" ")

            result["names"][entry_century].append(split_name[0])
            result["surnames"][entry_century].append(split_name[-1])

        for century in result["names"]:
            result["names"][century] = count_and_reduce(result["names"][century])

        for century in result["surnames"]:
            result["surnames"][century] = count_and_reduce(result["surnames"][century])

        return result

    def dist_by_relationship(self) -> dict[str, int]:

        relationship_exp = r'\,([\w\s]+)\. Proc'

        result: dict[str, int] = {}

        for entry in self.all:

            if entry["obs"] and (match := re.search(relationship_exp, entry["obs"])):

                rel = match[1]
                if rel not in result:
                    result[rel] = 0

                result[rel] += 1

        return result

    def as_json(self):
        return json.dumps(self.by_folder)


def count_and_reduce(name_list: list[str]) -> list[str]:
    counted_names: Counter = Counter(name_list)
    counted_names_as_list: list[tuple[str, int]] = [(elem, counted_names[elem]) for elem in counted_names]

    sorted_names: list[tuple[str, int]] = sorted(counted_names_as_list, key=lambda x: x[1], reverse=True)
    return [pair[0] for pair in sorted_names[:5]]


def get_century(year: int) -> int:
    if year <= 100:
        return 1

    elif year % 100 == 0:
        return year // 100

    else:
        return year // 100 + 1


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

    # data.dist_by_year()
    # data.dist_by_relationship()
    # data.dist_by_names()
    #
    # data.as_json()


if __name__ == '__main__':
    SystemExit(main())
