import sys
from typing import Callable

STARTED: bool = False
STATE: str = None
SALDO: int


def handle_levantar(_):

    global STARTED, STATE, SALDO
    STARTED = True
    STATE = "LEVANTAR"
    SALDO = 0

    print("machine> Insert coins.")


def handle_moeda(line: str):

    global STARTED, STATE, SALDO

    valid_coins: list[str] = ["2e", "1e", "50c", "20c", "10c", "5c", "2c", "1c"]

    if not STARTED:
        print("machine> You need to pick up the phone.")
        return

    if STATE != "LEVANTAR":
        print("machine> Invalid command!")
        return

    coins = [coin.strip() for coin in line[:-1].split(" ", 1)[1].split(",")]

    for coin in coins:
        if coin not in valid_coins:
            print(f"machine> Invalid coin: {coin}")
            return

    SALDO += sum([int(coin[:-1]) * 100 if coin.endswith("e") else int(coin[:-1]) for coin in coins])
    print(f"machine> Current balance: {SALDO // 100}e{SALDO % 100}c")

    STATE = "MOEDA"


def handle_telefone(line: str):

    global STARTED, STATE, SALDO

    if not STARTED:
        print("machine> You need to pick up the phone.")
        return

    if STATE != "MOEDA":
        print("machine> Invalid command!")
        return

    number: str = line.split(" ")[1]

    if number in ["601", "641"]:
        print("machine> This number is not allowed on this phone. Please dial a new number!")
        return

    if len(number) != 9:
        print("machine> Invalid number. Please dial a new number!")
        return

    if number.startswith("00"):

        if SALDO < 150:
            print("machine> You don't have enough balance to make this call. Please insert more coins!")
            return

        SALDO -= 150
        STATE = "T="

        print(f"machine> Call to {number} made successfully. Current balance: {SALDO // 100}e{SALDO % 100}c")
        return

    if number.startswith("2"):

        if SALDO < 25:
            print("machine> You don't have enough balance to make this call. Please insert more coins!")
            return

        SALDO -= 25
        STATE = "T="
        print(f"machine> Call to {number} made successfully. Current balance: {SALDO // 100}e{SALDO % 100}c")
        return

    if number.startswith("800"):
        STATE = "T="
        print(f"machine> Call to {number} made successfully. Current balance: {SALDO // 100}e{SALDO % 100}c")
        return

    if number.startswith("808"):

        if SALDO < 10:
            print("machine> You don't have enough balance to make this call. Please insert more coins!")
            return

        SALDO -= 10
        STATE = "T="

        print(f"machine> Call to {number} made successfully. Current balance: {SALDO // 100}e{SALDO % 100}c")
        return


def handle_abortar(_):
    sys.exit(0)

def handle(line: str):

    handles: dict = {
        "LEVANTAR": handle_levantar,
        "MOEDA": handle_moeda,
        "T=": handle_telefone,
        "ABORTAR": handle_abortar
    }

    handler: Callable[[str], None] = handles.get(line.split(" ")[0])

    if not handler:
        print("machine> Invalid command!")
        return

    handler(line)


def main():

    while True:
        line = str(input("user> "))
        handle(line.strip())


if __name__ == '__main__':
    SystemExit(main())
