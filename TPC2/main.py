import re


def main() -> int:

    on_pattern: str = r"on"
    off_pattern: str = r"off"
    number_pattern: str = r"([0-9]+)"

    result: int = 0
    state: bool = False

    while True:

        user_input: str = input("> ")

        matches = re.findall(on_pattern, user_input, re.IGNORECASE)
        if matches:
            state = True

        matches = re.findall(off_pattern, user_input, re.IGNORECASE)
        if matches:
            state = False

        if state:
            matches = re.findall(number_pattern, user_input)
            for number in matches:
                result += int(number)

            if '=' in user_input:
                print(f"sys> {result}")


if __name__ == '__main__':
    SystemExit(main())