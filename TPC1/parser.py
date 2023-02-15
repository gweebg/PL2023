
from time import perf_counter
import csv

from TPC1.storage import Entry, Storage

AGE_OR_TENSION = r"^(1\d{2}|[1-9]\d|\d)$"
SEX = r"^(M|F)$"
CHOLESTEROL = r"^([1-9]\d{0,2}|0)$"
BPM = r"^(?:[0-9]|[1-9][0-9]|[12][0-1][0-9]|220)$"
SICK = r"^(1|0)$"


class Parser:

    def __init__(self, source: str) -> None:

        self.source: str = source

    @staticmethod
    def is_valid(entry: list[str]) -> bool:
        """
        Validates an entry, using casting and conditionals.

        entry: list[str] = [idade, sexo, tensão, colesterol, batimento, temDoença]
                              0      1     2          3          4           5

        :param entry: Given entry to validate.
        :return: True if the data is valid, False otherwise.
        """

        age: int = int(entry[0])
        if age < 0 or age > 200:
            return False

        sex: str = entry[1]
        if sex not in ['M', 'F']:
            return False

        tension: int = int(entry[2])
        if tension < 0 or tension > 200:
            return False

        cholestrol: int = int(entry[3])
        if cholestrol < 0 or cholestrol > 1000:
            return False

        bpm: int = int(entry[4])
        if bpm < 0 or bpm > 300:
            return False

        has_desease: str = entry[5]
        if has_desease not in ["1", "0"]:
            return False

        return True

    def parse(self):

        data = Storage()

        with open(self.source, "r") as file:
            csv_reader = csv.reader(file)

            next(csv_reader)  # Skip the header line of the generator.

            for entry in csv_reader:
                if self.is_valid(entry):
                    data.add_entry(Entry.from_csv_entry(entry))

        return data


def main():
    parser = Parser("datasets/myheart.csv")

    start = perf_counter()
    data = parser.parse()
    stop = perf_counter()

    print(f"Finished in {stop - start}s")

    # data.dist_sick_by_gender(display=True)
    # data.dist_sick_by_age(display=True)


if __name__ == '__main__':
    SystemExit(main())
