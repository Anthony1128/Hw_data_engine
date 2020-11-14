import os
import shutil
import time
import pandas as pd
import numpy as np
import requests
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
import matplotlib.pyplot as plt
from random import randint
from hw_6.hw6_1.data_generator import data_generate

YEAR = 2019


# Preparing custom holidays from url
class RussianHolidays(AbstractHolidayCalendar):
    global YEAR
    url_holidays_calendar = f'http://jsoncalendar.ru/data/{YEAR}/calendar.json'

    rules = []
    holidays_json = requests.get(url_holidays_calendar).json()
    for holiday in holidays_json['days']:
        if holiday['type'] == 1:
            name = holiday['holiday_id']
            month = int(holiday['date_string'][:2])
            day = int(holiday['date_string'][3:])
            rules.append(Holiday(name, month=month, day=day))


# Counts implementation time from data frame
def get_implementation_time(data, holiday_calendar):
    timedelta_dict = {}
    for id_r, row in data.iterrows():
        name = row.name
        start_date = row['Start Date']
        end_date = row['End Date']

        delta = pd.Timedelta(days=1)
        if end_date.hour < 8:
            delta = pd.Timedelta(days=0)
        business_hours = pd.offsets.CustomBusinessHour(start='08:00', end='18:00', calendar=holiday_calendar)
        working_hours = pd.bdate_range(start_date, end_date + delta, freq=business_hours)
        if 8 <= end_date.hour < 18 and len(working_hours):
            i = len(working_hours) - 1
            while end_date.hour != working_hours[i].hour:
                i -= 1
            hours = i
            minutes = end_date.minute
        else:
            hours = len(working_hours)
            minutes = 0
        timedelta_dict[name] = pd.Timedelta(hours=hours, minutes=minutes)
    return timedelta_dict


# Adds new column to data frame with implementation time from dictionary
def add_column_to_df(data, timedelta_dict):
    data['Implementation time'] = pd.Series(timedelta_dict)
    return data


# Counts amount of dates from data frame by month
def count_dates_from_df(data):
    count_start_date = {}
    count_end_date = {}
    for id_r, row in data.iterrows():
        start_date = row['Start Date']
        if start_date.month in count_start_date:
            count_start_date[start_date.month] += 1
        else:
            count_start_date[start_date.month] = 1

        end_date = row['End Date']
        if end_date.month in count_end_date:
            count_end_date[end_date.month] += 1
        else:
            count_end_date[end_date.month] = 1

    count_dates = {}
    for month in range(1, 13):
        if month not in count_start_date.keys():
            count_start_date[month] = 0
        if month not in count_end_date.keys():
            count_end_date[month] = 0
        count_dates[month] = [count_start_date[month], count_end_date[month]]
    df_count_dates = pd.DataFrame.from_dict(count_dates,
                                            orient='index',
                                            columns=['Received',
                                                     'Implemented'])

    df_count_dates.index.rename('month', inplace=True)
    return df_count_dates.sort_values(by='month')


# Draws a histogram
def draw_hist(dataframe):
    return dataframe.plot(kind='bar')


def delete_catalog_recurs():
    shutil.rmtree('figures')


def main():
    N = randint(2, 2)
    os.mkdir('figures')
    rus_cal = RussianHolidays()
    perfomance_time = []
    for i in range(1, N+1):
        start_program_time = time.time()
        print(f'{i} of {N} dataframes')

        data = data_generate(10**i)
        implementation_dict = get_implementation_time(data, rus_cal)
        df_with_impl_time = add_column_to_df(data, implementation_dict)
        df_for_hist = count_dates_from_df(df_with_impl_time)
        fig = draw_hist(df_for_hist)
        fig.figure.savefig(f'figures/fig_{i}.svg')
        plt.close()

        perform_time = time.time() - start_program_time
        perfomance_time.append(perform_time)
        print(f'time of performance: {perform_time} seconds')

    plt.clf()
    df = pd.Series(perfomance_time)
    df.plot()
    plt.show()



if __name__ == '__main__':
    main()
    # delete_catalog_recurs()








