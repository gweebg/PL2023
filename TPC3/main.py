import re
import json

from typing import Optional, TypedDict
from pydantic import BaseModel
from collections import Counter


class Entry(TypedDict):

    """
    Attributes:
        folder (int): Identifies which folder the process belongs to.
        date (str): The date of the process as a string formatted like 'YYYY-mm-dd'.
        name (str): The name of the victim.
        father (Optional[str]): The name of the victims father.
        mother (Optional[str]): The name of the victims mother.
        obs (str): String containing various observations, the family relationship status or process identification.
    """

    folder: int
    date: str
    name: str
    father: Optional[str]
    mother: Optional[str]
    obs: Optional[str]


class Storage(BaseModel):

    """
    Attributes:
        all (list[Entry]): List of every entry, unordered.
        by_folder (dict[int, list[Entry]): Dictionary containing every entry by the folder number.
    """

    all: list[Entry]
    by_folder: dict[int, list[Entry]]

    def dist_by_year(self) -> dict[int, int]:
        """
        Distribution of processes by its year.
        :return: The distribution as a dictionary.
        """

        dist: dict[int, int] = {}

        for entry in self.all:

            if (year := int(entry["date"].split("-", 1)[0])) not in dist:
                dist[year] = 0

            dist[year] += 1

        return dist

    def dist_by_names(self) -> dict[str, dict[int, list[str]]]:
        """
        Distribution of the victims names over each century.
        :return: The distribution as a dictionary.
        """

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
        """
        Distribution of the family relationships (Sister, Brother, Nephew, etc.).
        :return: The distribuiton as a dictionary.
        """

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
        """
        :return: JSON object of the `by_folder` attribute.
        """
        return json.dumps(self.by_folder)


def count_and_reduce(name_list: list[str]) -> list[str]:
    """
    From a list only containing names, get the five most used ones.

    Example:
        l = ["name_c", "name_a", "name_b", "name_a"]
        l = [("name_c", 1), ("name_a", 2), ("name_b", 1)]
        l = ["name_a", "name_c", "name_b"]

    :param name_list: The list containing the names to be counted and ranked.
    :return: List containign the top five most used names.
    """

    counted_names: Counter = Counter(name_list)
    counted_names_as_list: list[tuple[str, int]] = [(elem, counted_names[elem]) for elem in counted_names]

    sorted_names: list[tuple[str, int]] = sorted(counted_names_as_list, key=lambda x: x[1], reverse=True)
    return [pair[0] for pair in sorted_names[:5]]


def get_century(year: int) -> int:
    """
    Retrieve the century from a year.
    :param year: The year (lol?).
    :return: The century (lol!?).
    """

    if year <= 100:
        return 1

    elif year % 100 == 0:
        return year // 100

    else:
        return year // 100 + 1


def pack_entry(match: Optional[re.Match]) -> Entry:
    """
    Packs a regex match into an Entry type object.
    :param match: Regex match.
    :return: Entry object.
    """

    return Entry(
        folder=int(match[1]), date=match[2], name=match[3],
        father=match[4], mother=match[5], obs=match[6]
    )


def parse(file_path: str) -> Storage:
    """
    Parses the file using regular expressions and generates a Storage type object containing organizes data.
    :param file_path: File path to the file to be parsed.
    :return: Storage object with the read data.
    """

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
