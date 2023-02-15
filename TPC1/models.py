from dataclasses import dataclass
from typing import Optional

import math


@dataclass
class Entry:
    age: int
    sex: str
    tension: int
    cholestrol: int
    bpm: int
    has_desease: bool

    @classmethod
    def from_csv_entry(cls, entry) -> 'Entry':
        return cls(int(entry[0]),
                   entry[1],
                   int(entry[2]),
                   int(entry[3]),
                   int(entry[4]),
                   bool(int(entry[5]))
                   )


class Storage:
    """
    Class that stores and organizes data from the csv file.
    """

    def __init__(self):
        """
        Class constructor.
        """

        self.age_ranges = 5  # Ranges to group the ages.
        self.max_age: int = 0  # The highest value for the age field.
        self.total_entries: int = 0  # The total of entries stored.

        # Dictionary containing entries organized by sickness, sex and age.
        self.__items = {
            "sick": {

                "M": {0: []},
                "F": {0: []}
            },

            "not_sick": {

                "M": {0: []},
                "F": {0: []}

            }
        }

    def get_group(self, age: int) -> int:
        return math.floor(age / self.age_ranges) * self.age_ranges

    def get_missing_ranges(self, latest_group: int, current_group: int) -> list[int]:
        return list(range(latest_group + self.age_ranges, current_group + self.age_ranges * 2, self.age_ranges))

    def add_entry(self, entry: Entry):

        entry_status: str = "not_sick"
        if entry.has_desease:
            entry_status = "sick"

        current_group: int = self.get_group(entry.age)

        if current_group > self.max_age:

            latest_group: int = self.get_group(self.max_age)

            if current_group > latest_group:

                missing_ranges: list[int] = self.get_missing_ranges(latest_group, current_group)

                for r in missing_ranges:
                    self.__items["sick"]["M"].update({r: []})
                    self.__items["sick"]["F"].update({r: []})
                    self.__items["not_sick"]["F"].update({r: []})
                    self.__items["not_sick"]["M"].update({r: []})

            self.max_age = entry.age

        self.__items[entry_status][entry.sex][current_group].append(entry)
        self.total_entries += 1

    def dist_sick_sex(self) -> dict:

        sick_males = sum([len(self.__items["sick"]["M"][q]) for q in self.__items["sick"]["M"]])
        sick_females = sum([len(self.__items["sick"]["F"][q]) for q in self.__items["sick"]["F"]])

        return {
            'M': sick_males,
            'F': sick_females,
            'T': self.total_entries
        }
