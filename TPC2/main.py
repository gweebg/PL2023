import re

from typing import Optional


def pure_resolution():

    while True:

        user_input: str = input("> ")
        state: bool = False
        result: int = 0

        for index, char in enumerate(user_input.strip()):

            next_char: Optional[str] = user_input[index + 1] if (index + 1 < len(user_input)) else None
            next_next_char: Optional[str] = user_input[index + 2] if (index + 2 < len(user_input)) else None

            if char.isnumeric() and state:
                result += int(char)

            if next_char and char in ['o', 'O'] and next_char in ['n', 'N']:
                state = True

            if next_next_char and char in ['o', 'O'] and next_char in ['f', 'F'] and next_next_char in ['f', 'F']:
                state = False

            if char == '=':
                print(f"sum> {result}")


if __name__ == '__main__':
    SystemExit(pure_resolution())
