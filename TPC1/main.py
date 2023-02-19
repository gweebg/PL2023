import parser
from TPC1.storage import Storage

from time import perf_counter


def validator(entry: list[str]) -> bool:
    return True


def main():
    start = perf_counter()
    storage: Storage = parser.read_csv("datasets/myheart.csv", validator)
    stop = perf_counter()

    print(f"Finished parsing in {stop - start}s")

    start = perf_counter()
    # storage.dist_sick_by_gender(display=True)
    results = storage.dist_sick_by_param_interval(interval=10, param="cholestrol", display=True)
    stop = perf_counter()

    print(f"Finished query in {stop - start}s")


if __name__ == '__main__':
    SystemExit(main())
