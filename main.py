from datetime import date, timedelta
from typing import List
import os
import datetime
import pandas as pd

# confirmed cases
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a9f182afe873ce7e65d2307fcf91013c23a4556c" \
      f"/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
dfC = pd.read_csv(url, error_bad_lines=False)

# deaths
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a9f182afe873ce7e65d2307fcf91013c23a4556c" \
      f"/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
dfD = pd.read_csv(url, error_bad_lines=False)

# recovered cases
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a9f182afe873ce7e65d2307fcf91013c23a4556c" \
      f"/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
dfR = pd.read_csv(url, error_bad_lines=False)


# Helper function
def format_date(date: datetime.date):
    if os.name == "nt":
        return date.strftime('%#m/%#d/%y')
    else:
        return date.strftime('%-m/%-d/%y')


def poland_cases_by_date(day: int, month: int, year: int = 2020) -> int:
    """
    Returns confirmed infection cases for country 'Poland' given a date.

    :param year: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param day: Day of month to get the cases for as an integer indexed from 1
    :param month: Month to get the cases for as an integer indexed from 1
    :return: Number of cases on a given date as an integer

    Ex.
    >>> poland_cases_by_date(7, 3, 2020)
    5
    >>> poland_cases_by_date(11, 3)
    31
    """

    return dfC.loc[dfC["Country/Region"] == "Poland"][format_date(date(year,month,day))].values[0]


def top5_countries_by_date(day: int, month: int, year: int = 2020) -> List[str]:
    """
    Returns the top 5 infected countries given a date (confirmed cases).

    :param day: 4 digit integer representation of the year to get the countries for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: A list of strings with the names of the coutires

    Ex.
    >>> top5_countries_by_date(27, 2, 2020)
    ['China', 'Korea, South', 'Cruise Ship', 'Italy', 'Iran']
    >>> top5_countries_by_date(12, 3)
    ['China', 'Italy', 'Iran', 'Korea, South', 'France']
    """

    dfCgrouped = dfC.groupby(by="Country/Region").sum()
    return dfCgrouped.sort_values(by=[format_date(date(year,month,day))], ascending=False).head(5).index.tolist()


def no_new_cases_count(day: int, month: int, year: int = 2020) -> int:
    """
    Returns the number of countries/regions where the infection count in a given day was the same as the previous day.
    :param day: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: Number of countries/regions where the count has not changed in a day

    Ex.
    >>> no_new_cases_count(11, 2, 2020)
    35
    >>> no_new_cases_count(3, 3)
    57
    """

    theday = date(year, month, day)
    beforeday = theday - timedelta(days=1)
    count = 0
    for index, row in dfC.iterrows():
        if row[format_date(theday)] != row[format_date(beforeday)]:
            count += 1
    return count


def countries_with_no_deaths_count(date: datetime.date) -> int:
    """
    Returns the number of areas (countries, region, provinces) in the data set
    where infections were found, but nobody died on a given date. (DO NOT GROUP BY)

    :param date: Date object of the date to get the results for
    :return: Number of countries with no deaths but with active cases on a given date as an integer

    Ex.
    >>> countries_with_no_deaths_count(datetime.date(2020, 3, 15))
    171
    >>> countries_with_no_deaths_count(datetime.date(2020, 2, 18))
    46
    """

    df = pd.DataFrame()
    df["confirmed"] = dfC[format_date(date)]
    df["deaths"] = dfD[format_date(date)]

    count = 0
    for index, row in df.iterrows():
        if row["confirmed"] > 0 and row["deaths"] == 0:
            count += 1
    return count


def more_cured_than_deaths_indices(date: datetime.date) -> List[int]:
    """
    Returns table indices of areas (countries, region, provinces) in the data set
    with more cured cases than deaths on a given date. (DO NOT GROUP BY)

    :param date: Date object of the date to get the results for
    :return: A List of integers containing indices of countries which had more cured cases than deaths on a given date

    Ex.
    >>> more_cured_than_deaths_indices(datetime.date(2020, 3, 15))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 19, 21, 24, 25, 27, 28, 29, 30, 32, 33, 34, 37, 38, 40, 41, 43, 44, 45, 46, 53, 55, 58, 59, 60, 62, 64, 65, 68, 86, 92, 101, 110, 118, 128, 154, 155, 156, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 187, 188, 189, 190, 191, 192, 193, 194, 202, 208]
    >>> more_cured_than_deaths_indices(datetime.date(2020, 2, 18))
    [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 15, 18, 19, 20, 92, 154, 156, 157, 158, 159, 160, 161, 162, 163, 164, 166, 167, 168, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 187, 188, 189, 190, 191, 192, 193, 194, 202, 347, 348, 403]
    """

    df = pd.DataFrame()
    df["deaths"] = dfD[format_date(date)]
    df["cured"] = dfR[format_date(date)]

    df = df.loc[df["deaths"] <  df["cured"]]
    return list(df.index)


def main():
    d = int(input("Enter a day: "))
    m = int(input("Enter a month: "))
    y = int(input("Enter a year: "))
    print(poland_cases_by_date(d, m, y))
    print(top5_countries_by_date(d, m, y))
    print(no_new_cases_count(d, m, y))

if __name__ == '__main__':
    main()
