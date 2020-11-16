import pandas as pd
import numpy as np
import random

YEAR = 2020


# Generates random Data Frame with n rows
def data_generate(n):
    data_array = []
    for i in range(n):
        start_date = start_date_generate(YEAR)
        end_date = end_date_generate(YEAR, start_date)
        data_array.append([i, start_date, end_date])
    np_array = np.array(data_array)
    df = pd.DataFrame(data=np_array,
                      columns=['Name', 'Start Date',
                               'End Date']).set_index('Name')
    return df


# Generates random start date
def start_date_generate(year):
    rd_month = random.randint(1, 12)
    if rd_month in [1, 3, 5, 7, 8, 10, 12]:
        rd_day = random.randint(1, 31)
    elif rd_month == 2:
        rd_day = random.randint(1, 28)
    else:
        rd_day = random.randint(1, 30)
    rd_hour = random.randint(0, 23)
    rd_minute = random.randint(0, 59)
    start_date = pd.Timestamp(year, rd_month, rd_day, rd_hour, rd_minute)
    return start_date


# Generates random end date
def end_date_generate(year, start_date):
    rd_month = random.randint(start_date.month, 12)
    if rd_month in [1, 3, 5, 7, 8, 10, 12]:
        rd_day = random.randint(1, 31)
        if rd_month == start_date.month:
            rd_day = random.randint(start_date.day, 31)
    elif rd_month == 2:
        rd_day = random.randint(1, 28)
        if rd_month == start_date.month:
            rd_day = random.randint(start_date.day, 28)
    else:
        rd_day = random.randint(1, 30)
        if rd_month == start_date.month:
            rd_day = random.randint(start_date.day, 30)

    rd_hour = random.randint(0, 23)
    if rd_month == start_date.month and rd_day == start_date.day:
        rd_hour = random.randint(start_date.hour, 23)
    rd_minute = random.randint(0, 59)
    if (rd_month == start_date.month and rd_day == start_date.day
            and rd_hour == start_date.hour):
        rd_minute == random.randint(start_date.minute, 59)
    end_date = pd.Timestamp(year, rd_month, rd_day, rd_hour, rd_minute)
    return end_date







