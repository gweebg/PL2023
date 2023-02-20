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
            "healthy_males": healthy_males,
            "healthy_females": healthy_females,
            "total_males": sick_males + healthy_males,

            "sick_males": sick_males,
            "sick_females": sick_females,
            "total_females": sick_females + healthy_females
        }

    def dist_sick_by_param_interval(self, interval: int = 5, param: str = "age", display: bool = False) -> dict:
        """
        Calculate the distribution of the desease by age intervals.

        :param param: Distribution by this parameter.
        :param interval: The interval size.
        :param display: Enable/disable plot visualization.
        :return: Dictionary with the distribution data.
        """

        key: str = "age_sorted"

        if param == "cholestrol":
            key = "col_sorted"

        # Query computing.
        sick: list[int] = list(map(lambda e: getattr(e, param), self.data["sick"][key]))
        healthy: list[int] = list(map(lambda e: getattr(e, param), self.data["healthy"][key]))

        range_limit: int = max(sick + healthy)

        filtered_sick = self.__filter_by_param__(sick, interval, range_limit)
        filtered_healthy = self.__filter_by_param__(healthy, interval, range_limit)

        # Display the graph.
        if display:
            self.display_interval_as_bar_plot(filtered_sick, filtered_healthy, param)

        return {
            "sick": filtered_sick,
            "total_sick": len(sick),
            "healthy": filtered_healthy,
            "total_healthy": len(healthy)
        }

    def __filter_by_param__(self, values: list[int], interval: int, range_limit: int) -> dict:
        """
        Filters a list of sorted ages into their respective bins (age intervals).

        :param values: List containing the values sorted from least to greater.
        :param interval: The size of interval.
        :param range_limit: The max value registered on the values list.
        :return: Dictionary with the intervals with the respective amount of people.
        """

        result: dict = {}

        superior_limit_group: int = self.__get_group__(range_limit, interval)
        ranges: list[int] = self.__get_ranges__(-interval, superior_limit_group, interval)

        # Initialize the resulting dictionary with every range with 0.
        for r in ranges:
            interval_fmt: str = f"[{r}-{r + interval}["
            result[interval_fmt] = 0

        # Sort the values by their 'bins'.
        for value in values:
            group: int = self.__get_group__(value, interval)
            interval_fmt: str = f"[{group}-{group + interval}["
            result[interval_fmt] += 1

        return result

    # Display #

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
        ax2.set_title(
            f"Females ({sick_females + healthy_females} Total)\nSick: {sick_females}, Healthy: {healthy_females}")
        ax2.legend(["Has Desease", "Healthy"])

        plot.show()

    @staticmethod
    def display_interval_as_bar_plot(sick: dict, healthy: dict, param: str = "age") -> None:
        """
        Display the distribution as a bar graph.

        :param param: Parameter to use.
        :param sick: Number of sick people per parameter interval.
        :param healthy: Number of healthy people per parameter interval.
        :return: None
        """

        keys = sick.keys()

        sick_values = sick.values()
        healthy_values = healthy.values()

        # Plotting the data.
        bar_width = 0.35

        fig, ax = plot.subplots()

        xaxis = np.arange(len(keys))

        sick_bar = ax.bar(xaxis - 0.2, sick_values, width=bar_width, label='Sick')
        healthy_bar = ax.bar(xaxis + 0.2, healthy_values, width=bar_width, label='Healthy')

        plot.xticks(xaxis, keys)
        plot.xlabel(f"{param.title()} Intervals")
        plot.ylabel("Number of People")
        plot.title("Distribution of the desease by {param} intervals.")

        plot.bar_label(sick_bar, fmt='%.2f')
        plot.bar_label(healthy_bar, fmt='%.2f')

        fig.tight_layout()

        plot.legend()
        plot.show()

    # Helpers #

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
