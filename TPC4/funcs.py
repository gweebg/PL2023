
def as_number_list(values: str, delimiter: str):
    return [float(elem) for elem in values.split(delimiter)]


def csv_sum(values: str, delimiter: str):
    return sum(as_number_list(values, delimiter))


def csv_avg(values: str, delimiter: str):
    return csv_sum(values, delimiter) / (values.count(delimiter) + 1)


def csv_max(values: str, delimiter: str):
    return max(as_number_list(values, delimiter))


def csv_min(values: str, delimiter: str):
    return min(as_number_list(values, delimiter))


def csv_concat(values: str, delimiter: str):
    return "".join([elem for elem in values.split(delimiter)])

