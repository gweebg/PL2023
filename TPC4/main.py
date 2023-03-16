import re

from pathlib import Path
from typing import Callable

from funcs import *

AVAILABLE_FUNCTIONS = {
    "sum": csv_sum,
    "avg": csv_avg,
    "max": csv_max,
    "min": csv_min,
    "concat": csv_concat
}


def gen_expression_from_header(header: list[tuple[str, str, str]]) -> str:

    expression: str = r""
    occurrences: tuple[int, int] = (1, 1)

    for part in header:

        if match := re.match(r"{(\d+)}", part[1]):
            occurrences = (int(match[1]), int(match[1]))

        elif match := re.match(r"{(\d+),(\d+)}", part[1]):

            if match[1] >= match[2]:
                raise Exception(f"Invalid range, left number need to be smaller than the right: {part[1]}")

            occurrences = (int(match[1]), int(match[2]))

        if occurrences[0] == occurrences[1]:

            if occurrences[0] == 1:
                expression += r"([\wà-üÀ-Ü\s.]+),"
            else:
                expression += r"(" + (r"[\wà-üÀ-Ü\s.]+," * occurrences[0])[:-1] + r")"

        else:
            expression += r"(" + (r"[\wà-üÀ-Ü\s.]+," * occurrences[0]) + (r"(?:[\wà-üÀ-Ü\s.]+,)?" * (occurrences[1] - occurrences[0])) + r")"

    return expression[0:(len(expression) - 4):] + expression[(len(expression) - 4) + 1::] + r"$"


def get_functions_from_header(header: list[tuple[str, str, str]]) -> dict[int, str]:

    result: dict[int, str] = {}

    for index, part in enumerate(header):
        if part[2][2:] in AVAILABLE_FUNCTIONS:
            result[index] = part[2][2:]

    return result


def apply_func(func: Callable[[str, str], any], on: str, delimiter: str) -> any:
    return func(on, delimiter)


def csv_to_json(csv_file: Path, delimiter: str = ","):
    """
    Lines can either be:

        Número,Nome,Curso
        Número,Nome,Curso{2},,
        Número,Nome,Curso{3,5},,,,,
        Número,Nome,Curso{2,4}::sum,,,,

    :return: Converted csv file as json.
    """

    result: list[dict] = []

    header_expr: str = r'([\wà-üÀ-Ü]+(?:({\d+}|{\d+,\d+})(::\w+)?)?)'

    with open(csv_file, 'r') as file:
        lines: list[str] = [line for line in file.readlines() if line]

    header = lines.pop(0)
    header = re.findall(header_expr, header)

    if not header:
        raise Exception(f"The header is not valid: {header}")

    row_expr: str = gen_expression_from_header(header)
    row_func: dict[int, str] = get_functions_from_header(header)

    print(row_expr)

    for line in lines:

        if match := re.match(row_expr, line):
            for index, elem in enumerate(match.groups()):

                obj: dict = {}

                if index in row_func:
                    obj[header[index][0]] = apply_func(AVAILABLE_FUNCTIONS[row_func[index]], elem, delimiter)

                else:
                    obj[header[index][0]] = [e for e in elem.split(delimiter)]

                result.append(obj)

    return result


def main():
    result = csv_to_json(Path("./dataset.csv"))
    print(result)


if __name__ == '__main__':
    SystemExit(main())
