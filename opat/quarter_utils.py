import datetime
from collections import namedtuple

Quarter = namedtuple("Quarter", "year,period")


class Quarter(object):
    year = None
    period = None
    _start = None
    _end = None

    def __init__(self, year, period):
        if not year or not period:
            raise ValueError(
                "A period and a year are required to construct a quarter"
            )
        self.year = year
        self.period = period

    def __eq__(self, y):
        return self.year == y.year and self.period == y.period

    @property
    def start(self):
        if not self._start:
            self._start, self._end = get_start_end_from_quarter(
                self.year, self.period
            )
        return self._start

    @property
    def end(self):
        if not self._end:
            self._start, self._end = get_start_end_from_quarter(
                self.year, self.period
            )
        return self._end

    @classmethod
    def from_date(cls, some_date):
        year = some_date.year
        for i in range(4):
            period = i + 1
            start, end = get_start_end_from_quarter(
                year, period
            )
            if some_date > start and some_date < end:
                return cls(year, period)

    def previous(self):
        if self.period == 1:
            return Quarter(self.year - 1, 4,)
        else:
            return Quarter(self.year, self.period - 1,)


def get_start_end_from_quarter(year, period):
    """
    if given a year and a quarter
    return the start/end inclusive

    expects a quarter (1-4)
    """
    if period == 1:
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 3, 31)
    elif period == 2:
        start_date = datetime.date(year, 4, 1)
        end_date = datetime.date(year, 6, 30)
    elif period == 3:
        start_date = datetime.date(year, 7, 1)
        end_date = datetime.date(year, 9, 30)
    else:
        start_date = datetime.date(year, 10, 1)
        end_date = datetime.date(year, 12, 31)

    return start_date, end_date


def get_previous_quarters(amount):
    quarter = Quarter.from_date(
        datetime.date.today()
    )
    quarters = []
    for i in xrange(amount):
        quarter = quarter.previous()
        quarters.append(quarter)
    return quarters
