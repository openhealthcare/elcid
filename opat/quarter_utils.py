import datetime


def get_start_end_from_quarter(year, quarter):
    """
    if given a year and a quarter
    return the start/end inclusive

    expects a quarter (1-4)
    """
    if quarter == 1:
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 3, 31)
    elif quarter == 2:
        start_date = datetime.date(year, 4, 1)
        end_date = datetime.date(year, 6, 30)
    elif quarter == 3:
        start_date = datetime.date(year, 7, 1)
        end_date = datetime.date(year, 9, 30)
    else:
        start_date = datetime.date(year, 10, 1)
        end_date = datetime.date(year, 12, 31)

    return start_date, end_date


def get_quarter_from_date(some_date):
    """
    returns the quarter (1-4) for a date
    """
    year = some_date.year
    for i in range(4):
        quarter = i + 1
        start, end = get_start_end_from_quarter(
            year, quarter
        )
        if some_date > start and some_date < end:
            return (year, quarter,)


def get_previous_quarter(year, quarter):
    if quarter == 1:
        return (year - 1, 4,)
    else:
        return (year, quarter - 1,)


def get_previous_quarters(amount):
    quarter = get_quarter_from_date(
        datetime.date.today()
    )
    quarters = []
    for i in xrange(amount):
        quarter = get_previous_quarter(*quarter)
        quarters.append(quarter)
    return quarters
