import os
import shutil
import time
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from random import randint
import logging
from data_generator import data_generate, YEAR

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.getLogger('matplotlib.font_manager').disabled = True


# Preparing custom holidays from url
def get_custom_holidays(year):
    url_holidays_calendar = f'http://jsoncalendar.ru/data/{year}/calendar.json'

    custom_holidays_np = []
    holidays_json = requests.get(url_holidays_calendar).json()
    for holiday in holidays_json['days']:
        if holiday['type'] == 1:
            month = int(holiday['date_string'][:2])
            day = int(holiday['date_string'][3:])
            custom_holidays_np.append(pd.Timestamp(YEAR, month, day).date())
    return custom_holidays_np


CUSTOM_HOLIDAYS_CALENDAR = get_custom_holidays(YEAR)


def is_business_day(date):
    return bool(len(pd.bdate_range(date, date, freq='C',
                                   holidays=CUSTOM_HOLIDAYS_CALENDAR)))


# Counts business time between two dates and amount of dates by month
def get_implementation_time(start_date, end_date, count_dates):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    busdays = np.busday_count(start_date.date(), end_date.date(),
                              holidays=CUSTOM_HOLIDAYS_CALENDAR)
    hours = busdays * 10
    minutes = 0

    if is_business_day(start_date):
        if 8 < start_date.hour < 18:
            hours -= start_date.hour - 8
            if start_date.minute != 0:
                hours -= 1
                minutes += 60 - start_date.minute
        elif start_date.hour > 18:
            hours -= 10
    if is_business_day(end_date):
        if 8 < end_date.hour < 18:
            hours += end_date.hour - 8
            minutes += end_date.minute
        elif end_date.hour > 18:
            hours += 10
    count_dates[start_date.month][0] += 1
    count_dates[end_date.month][1] += 1

    return pd.Timedelta(hours=hours, minutes=minutes)


# saves svg files with histogram in 'figures' catalog
def histogram_for_df(count_dates_dict, i, N):
    df_count_dates = pd.DataFrame.from_dict(count_dates_dict,
                                            orient='index',
                                            columns=['Received',
                                                     'Implemented'])

    df_count_dates.index.rename('month', inplace=True)
    df_for_hist = df_count_dates.sort_values(by='month')

    fig = df_for_hist.plot(kind='bar', title=f'{i} of {N} dataframes')
    plt.xticks(rotation=0, horizontalalignment="center")
    plt.ylabel("Amount")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    plt.xticks(np.arange(12), months)
    fig.figure.savefig(f'figures/fig_{i}.svg')
    plt.clf()
    plt.close()


# Displays 'Dependency of performance speed on N' graph
def create_graph(performance_time, N):
    plt.clf()
    df = pd.Series(performance_time)
    df.plot(title='Dependency of performance speed on N')
    plt.xticks(rotation=0, horizontalalignment="center")
    plt.xlabel("N")
    plt.ylabel("Performance speed (s)")
    plt.xlim(1)
    plt.xticks(np.arange(1, N + 1))
    plt.show()


# removes given catalog with its content
def delete_catalog_recurs(catalog):
    shutil.rmtree(catalog)


def main():
    N = randint(1, 6)

    # create folder for saving files with histograms there
    try:
        os.mkdir('figures')
    except FileExistsError as e:
        logging.info(e)
        pass

    # a list with performance time of each cycle
    performance_time = [0]

    for i in range(1, N+1):
        start_program_time = time.time()
        logging.info(f'{i} of {N} dataframes')

        data = data_generate(10**i)

        # dictionary to store the statistic by month
        count_dates_dict = {i: [0, 0] for i in range(1, 13)}

        vec_get_implementation_time = np.vectorize(get_implementation_time)
        time_deltas_array = vec_get_implementation_time(data['Start Date'],
                                                        data['End Date'],
                                                        count_dates_dict)
        data['Implementation time'] = time_deltas_array

        # clear out affect of np.vectorize cache (doubles 1st line of data)
        count_dates_dict[data['Start Date'][0].month][0] -= 1
        count_dates_dict[data['End Date'][0].month][1] -= 1

        histogram_for_df(count_dates_dict, i, N)

        perform_time = time.time() - start_program_time
        performance_time.append(perform_time)
        logging.info(f'time of performance: {perform_time} seconds')

    create_graph(performance_time, N)


if __name__ == '__main__':
    main()
    # delete_catalog_recurs('figures')







