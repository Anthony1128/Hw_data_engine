import pandas as pd
import numpy as np
import requests
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
import matplotlib.pyplot as plt
# from hw_6.hw6_1.data_generator import data_generate

YEAR = 2020

# DATA = data_generate(10)
np_ar = np.array([[5, pd.Timestamp(2020, 1, 2, 8, 0), pd.Timestamp(2020, 1, 10, 10, 0)],
                  [0, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 1, 18, 0)],
                  [1, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 2, 9, 30)],
                  [2, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 5, 19, 00)],
                  [3, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 12, 5, 8, 30)],
                  [4, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 1, 8, 0)]
                  ])
DATA = pd.DataFrame(data=np_ar,
                    columns=['Name', 'Start Date',
                             'End Date']).set_index('Name')


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
        print(working_hours)
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
    print(timedelta_dict)
    return timedelta_dict


# Adds new column to data frame with implementation time
def add_column_to_df(data):
    rus_cal = RussianHolidays()
    timedelta_dict = get_implementation_time(data, rus_cal)
    data['Implementation time'] = pd.Series(timedelta_dict)
    return data


# Counts amount of dates from data frame by month
def count_dates_from_df(data):
    count_start_date = {}
    count_end_date = {}
    data = add_column_to_df(data)

    for id_r, row in data.iterrows():
        start_date = row[0]
        if start_date.month in count_start_date:
            count_start_date[start_date.month] += 1
        else:
            count_start_date[start_date.month] = 1

        end_date = row[1]
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
    print(data)
    return df_count_dates.sort_values(by='month')


# Draws a histogram
df = count_dates_from_df(DATA)
# df.plot(kind='bar')
# plt.show()









