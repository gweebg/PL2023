def tabulate_interval(query_result: dict, description: str) -> None:
    header_values: list[str] = ["Sick", "Healthy"]
    header_row: str = "+" + ("-" * 12) + ("-" * sum([len(i) for i in header_values])) + ("-" * 6) + "+"
    header_val: str = "|" + (" " * 12) + "| " + header_values[0] + " | " + header_values[1] + " |"

    print(header_row)
    print(header_val)
    print(header_row)

    intervals: list[str] = list(query_result["sick"].keys())

    for interval in intervals:

        sick_value: int = query_result["sick"][interval]
        healthy_value: int = query_result["healthy"][interval]

        if sick_value != 0 or healthy_value != 0:
            row: str = "| " + interval + (" " * (10 - len(interval))) + " | " + \
                       (str(sick_value) + " " * (4 - len(str(sick_value)))) + " | " + \
                       str(healthy_value) + " " * (7 - len(str(healthy_value))) + " |"

            print(row)
            print(header_row)

    totals: str = "| Total      " + "| " + \
                  str(query_result['total_sick']) + " " * (4 - len(str(query_result['total_sick']))) + " | " + \
                  str(query_result['total_healthy']) + " " * (7 - len(str(query_result['total_healthy']))) + " |"

    print(totals)
    print(header_row)
    print(description)
    print("(Note that empty intervals are ignored.)")


def tabulate_gender(query_result: dict, description: str) -> None:

    header_values: list[str] = ["Sick", "Healthy"]
    header_row: str = "+" + ("-" * 8) + ("-" * sum([len(i) for i in header_values])) + ("-" * 6) + "+"
    header_val: str = "|" + (" " * 8) + "| " + header_values[0] + " | " + header_values[1] + " |"

    print(header_row)
    print(header_val)
    print(header_row)

    male_row: str = "| Male   | " \
                    + str(query_result['sick_males']) + " " * (4 - len(str(query_result['sick_males']))) \
                    + " | " + str(query_result['healthy_males']) + \
                    " " * (6 - len(str(query_result['sick_males']))) + "  |"

    female_row: str = "| Female | " \
                      + str(query_result['sick_females']) + " " * (4 - len(str(query_result['sick_females']))) \
                      + " | " + str(query_result['healthy_females']) + \
                      " " * (6 - len(str(query_result['sick_females']))) + " |"

    print(male_row)
    print(header_row)
    print(female_row)
    print(header_row)
    print(description)
