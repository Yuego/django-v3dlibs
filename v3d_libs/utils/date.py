#coding: utf-8
from __future__ import unicode_literals, absolute_import

import calendar


def get_total_year_days(year):
    return sum(map(lambda x: calendar.monthrange(year, x)[1], range(1, 13)))


def get_current_year_days(year, month, day):
    start = sum(map(lambda x: calendar.monthrange(year, x)[1], range(1, month)))
    return start + day


def get_rng(year, month, day):
    return get_total_year_days(year) - get_current_year_days(year, month, day);


def get_pay(summ, year, month, day):
    total = get_total_year_days(year)
    diff = get_rng(year, month, day)

    return (float(summ) / total) * diff
