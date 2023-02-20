import os
from typing import Callable

import parser

from TPC1.storage import Storage

from TPC1.tables import tabulate_interval, tabulate_gender


def validator(entry: list[str]) -> bool:
    return True


class Interface:

    def __init__(self, inital_path: str):

        self.path = inital_path

        self.storage: Storage = parser.read_csv(self.path, validator)

        self.plot: bool = False
        self.tables: bool = True

        self.commands: dict = {

            "help": self.handle_help,
            "plot": self.handle_plot,
            "tables": self.handle_tables,
            "load": self.handle_load,
            "dist": self.handle_dist

        }

    @staticmethod
    def handle_help(_) -> None:

        print("system> Available commands:")
        print("        help - Displays this message on the screen.")
        print("        plot {on|off} - Enables or disables the display of plots for the distributions.")
        print("        tables {on|off} - Enables or disables the display of tables for the distributions.")
        print("        load {file-path} - Change the current data set to the indicated by 'file-path'.")
        print("        dist {gender|age|cholestrol} - Computes the distribution for the indicated query.")

    def handle_dist(self, user_input: list[str]):

        query: str = user_input[1]

        if query not in ["gender", "age", "cholestrol"]:
            print(f"dist.error> Invalid argument {query}.")
            return

        if query == "gender":
            result: dict = self.storage.dist_sick_by_gender(display=self.plot)

            if self.tables:
                tabulate_gender(result, "Desease distribution by gender.")

            return

        if query in ["age", "cholestrol"]:
            result: dict = self.storage.dist_sick_by_param_interval(param=query, display=self.plot)

        if self.tables:
            tabulate_interval(result, f"Desease distribution by the {query}.")

    def handle_load(self, user_input: list[str]):

        path: str = user_input[1]

        if not os.path.isfile(path):
            print(f"load.error> The file {path} does not exist.")
            return

        self.path = path
        self.storage = parser.read_csv(self.path, validator)

        print(f"system> Loaded with sucsess file {path}.")

    def handle_tables(self, user_input: list[str]) -> None:

        arg: str = user_input[1]

        if arg not in ["on", "off"]:
            print("tables.error> Invalid command argument, check the help menu.")
            return

        if arg == "on":
            self.tables = True
        else:
            self.tables = False

        print(f"system> Table display is now set to {arg}.")

    def handle_plot(self, user_input: list[str]) -> None:

        arg: str = user_input[1]

        if arg not in ["on", "off"]:
            print("plot.error> Invalid command argument, check the help menu.")
            return

        if arg == "on":
            self.plot = True
        else:
            self.plot = False

        print(f"system> Plot generation is now set to {arg}.")

    def handle_input(self, user_input: list[str]) -> None:

        command: str = user_input[0]

        if command not in self.commands:
            print(f"error> Command {command} does not exist.")
            return

        if len(user_input) > 2:
            print(f"error> Too many arguments.")
            return

        executor: Callable = self.commands[command]
        executor(user_input)

    def run(self):

        print("Welcome to Query Visualizer 3000!")
        print("You can check all the commands by using the 'help' command!")

        while True:

            user_input: str = input("command> ")

            try:
                command: str = user_input.split(" ")[0]
                self.handle_input(user_input.split(" "))

            except IndexError:
                print("error> Please insert a valid command, use the 'help' command to check them all.")


def main():
    ui = Interface(inital_path="./datasets/myheart.csv")

    try:
        ui.run()

    except KeyboardInterrupt:
        print("\nsystem> Goodbye!")


if __name__ == '__main__':
    SystemExit(main())
