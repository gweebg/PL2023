import matplotlib.pyplot as plot
import numpy as np

from math import floor

from TPC1.models import Entry


class Storage:
    """
    Class that stores and organizes data from the csv file.
    """

    def __init__(self):
        """
        Class constructor.
        """

        self.total_entries: int = 0

        self.data = {

            "healthy": {
                "M": [],
                "F": [],
                "age_sorted": [],
                "col_sorted": []
            },

            "sick": {
                "M": [],
                "F": [],
                "age_sorted": [],
                "col_sorted": []
            },

        }

    @staticmethod
    def is_sick(entry: Entry) -> str:
        return "sick" if entry.has_desease else "healthy"

    def add(self, entry: Entry) -> None:
        """
        Insert an entry into the storage.
        :param entry: Entry of type Entry to add.
        :return: None
        """
        status: str = self.is_sick(entry)

        self.data[status][entry.sex].append(entry)
        self.data[status]["age_sorted"].append(entry)
        self.data[status]["col_sorted"].append(entry)

    def finish(self) -> None:
        """
        Clean up data and sort the needed lists.
        :return: None
        """

        self.data["sick"]["age_sorted"].sort(key=lambda e: e.age)
        self.data["sick"]["col_sorted"].sort(key=lambda e: e.cholestrol)

        self.data["healthy"]["age_sorted"].sort(key=lambda e: e.age)
        self.data["healthy"]["col_sorted"].sort(key=lambda e: e.cholestrol)

    def dist_sick_by_gender(self, display: bool = False) -> dict:
        """
        Calculate the distribution of sick people by their gender.

        :param display: Enable/disable plot visualization.
        :return: Dictionary with the distribution data.
        """

        sick_males: int = len(self.data["sick"]["M"])
        sick_females: int = len(self.data["sick"]["F"])

        healthy_males: int = len(self.data["healthy"]["M"])
        healthy_females: int = len(self.data["healthy"]["F"])

        if display:
            self.display_gender(sick_males, sick_females, healthy_males, healthy_females)

        return {
            "healthy": {
                "M": healthy_males,
                "F": healthy_females
            },

            "sick": {
                "M": sick_males,
                "F": sick_females
            },

            "total_males": sick_males + healthy_males,
            "total_females": sick_females + healthy_females
        }

    @staticmethod
    def display_gender(sick_males, sick_females, healthy_males, healthy_females) -> None:
        """
        Display on a pie chart, the distribution of the desease by the gender.

        :param sick_males: Number of sick males.
        :param sick_females: Number of sick females.
        :param healthy_males: Number of healthy males.
        :param healthy_females: Number of healthy females.
        :return: None
        """

        fig, (ax1, ax2) = plot.subplots(1, 2, figsize=(10, 5))

        fig.suptitle("Distribution of the desease by gender.")

        ax1.pie([sick_males, healthy_males], autopct='%1.1f%%')
        ax1.set_title(f"Males ({sick_males + healthy_males} Total)\nSick: {sick_males}, Healthy: {healthy_males}")
        ax1.legend(["Has Desease", "Healthy"])

        ax2.pie([sick_females, healthy_females], autopct='%1.1f%%')
        ax2.set_title(f"Females ({sick_females + healthy_females} Total)\nSick: {sick_females}, Healthy: {healthy_females}")
        ax2.legend(["Has Desease", "Healthy"])

        plot.show()

    def dist_sick_by_age(self, age_interval: int = 5, display: bool = False) -> dict:
        """
        Calculate the distribution of the desease by age intervals.

        :param age_interval: The interval size.
        :param display: Enable/disable plot visualization.
        :return: Dictionary with the distribution data.
        """

        # Query computing.
        sick_ages: list[int] = list(map(lambda e: e.age, self.data["sick"]["age_sorted"]))
        healthy_ages: list[int] = list(map(lambda e: e.age, self.data["healthy"]["age_sorted"]))

        max_age: int = max(sick_ages + healthy_ages)

        sick_by_ages = self.__filter_ages__(sick_ages, age_interval, max_age)
        healthy_by_ages = self.__filter_ages__(healthy_ages, age_interval, max_age)

        # Display the graph.
        if display:
            self.display_ages(sick_by_ages, healthy_by_ages)

        return {
            "sick": sick_by_ages,
            "healthy": healthy_by_ages,
            "total_sick": len(sick_ages),
            "total_healthy": len(healthy_ages)
        }

    @staticmethod
    def display_ages(sick: dict, healthy: dict) -> None:
        """
        Display the distribution as a bar graph.

        :param sick: Number of sick people per age interval.
        :param healthy: Number of healthy people per age interval.
        :return: None
        """

        keys = sick.keys()
        sick_values = sick.values()
        healthy_values = healthy.values()

        plot.figure(figsize=(20, 10))
        xaxis = np.arange(len(keys))

        sick_bar = plot.bar(xaxis - 0.2, sick_values, 0.4, label='Sick')
        healthy_bar = plot.bar(xaxis + 0.2, healthy_values, 0.4, label='Healthy')

        plot.xticks(xaxis, keys)
        plot.xlabel("Age Intervals")
        plot.ylabel("Number of People")
        plot.title("Distribution of the desease by age intervals.")

        plot.bar_label(sick_bar, fmt='%.2f')
        plot.bar_label(healthy_bar, fmt='%.2f')

        plot.legend()
        plot.show()

    def __filter_ages__(self, ages: list[int], age_interval: int, superior_limit: int) -> dict:
        """
        Filters a list of sorted ages into their respective bins (age intervals).

        :param ages: List containing the ages sorted from least to greater.
        :param age_interval: The size of interval.
        :param superior_limit: The max age registered on the ages list.
        :return: Dictionary with the intervals with the respective amount of people.
        """

        result: dict = {}

        superior_limit_group: int = self.__get_group__(superior_limit, age_interval)
        ranges: list[int] = self.__get_ranges__(-age_interval, superior_limit_group, age_interval)

        for r in ranges:
            interval: str = f"[{r}-{r + age_interval}["

            result[interval] = 0
            result[interval] += len(list(filter(lambda e: r <= e < r + age_interval, ages)))

        return result

    @staticmethod
    def __get_group__(age: int, age_interval: int) -> int:
        """
        Returns the interval of which the provided age bellongs to, the interval is defined by age_ranges.

        Example:
            $> __get_group__(13)
            $> 10

        :param age: The age to retrieve the group from.
        :param age_interval: Age interval.
        :return: The group as integer.
        """
        return floor(age / age_interval) * age_interval

    @staticmethod
    def __get_ranges__(latest_group: int, current_group: int, age_interval: int) -> list[int]:
        """
        Generate a list with the intervals needed to be created on the database.

        Example:
            $> __get_missing_ranges__(5, 40)
            $> [10, 15, 20, 25, 30, 35, 40]

        :param latest_group: Lowest bound.
        :param current_group: Highest bound.
        :return: List with the intervals needed to be created.
        """
        return list(range(latest_group + age_interval, current_group + age_interval, age_interval))
