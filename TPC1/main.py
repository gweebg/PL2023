import parser
from TPC1.storage import Storage

from time import perf_counter


def validator(entry: list[str]) -> bool:
    return True


def main():
    start = perf_counter()
    storage: Storage = parser.read_csv("datasets/myheart.csv", validator)
    stop = perf_counter()

    print(f"Finished in {stop - start}s")

    storage.dist_sick_by_gender(display=True)
    storage.dist_sick_by_age(display=True)


if __name__ == '__main__':
    SystemExit(main())
