import pandas as pd
import numpy as np
import requests
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
import matplotlib.pyplot as plt
from hw_6.hw6_1.data_generator import data_generate


DATA = data_generate(10)
# np_ar = np.array([[0, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 1, 18, 0)],
#                   [1, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 2, 9, 30)],
#                   [2, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 5, 8, 30)],
#                   [3, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 12, 5, 8, 30)]])
# DATA = pd.DataFrame(data=np_ar,
#                     columns=['Name', 'Start Date',
#                              'End Date']).set_index('Name')
YEAR = 2020


class RussianHolidays(AbstractHolidayCalendar):
    global YEAR
    url_calendar = f'http://jsoncalendar.ru/data/{YEAR}/calendar.json'

    rules = []
    holidays_json = requests.get(url_calendar).json()
    for holiday in holidays_json['days']:
        if holiday['type'] == 1:
            name = holiday['holiday_id']
            month = int(holiday['date_string'][:2])
            day = int(holiday['date_string'][3:])
            rules.append(Holiday(name, month=month, day=day))


def implementation(data):
    result = {}
    for id_r, row in data.iterrows():
        start_date = row[0]
        end_date = row[1]

        delta = pd.Timedelta(days=1)
        if end_date.hour < 8:
            delta = pd.Timedelta(days=0)
        rus_cal = RussianHolidays()
        bh = pd.offsets.CustomBusinessHour(start='08:00', end='18:00', calendar=rus_cal)
        working_hours = pd.bdate_range(start_date, end_date + delta, freq=bh)

        if 8 <= end_date.hour < 18:
            i = len(working_hours) - 1
            while end_date.hour != working_hours[i].hour:
                i -= 1
            hours = i
            minutes = end_date.minute
        else:
            hours = len(working_hours)
            minutes = 0
        result[pd.Timedelta(hours=hours, minutes=minutes)] = id_r
    return result


def add_column(data):
    result = implementation(DATA)
    data['Implementation time'] = result
    return data


def df_month():
    statistic_get = {}
    statistic_end = {}
    data = add_column(DATA)

    for id_r, row in data.iterrows():
        start_date = row[0]
        if start_date.month in statistic_get:
            statistic_get[start_date.month] += 1
        else:
            statistic_get[start_date.month] = 1

        end_date = row[1]
        if end_date.month in statistic_end:
            statistic_end[end_date.month] += 1
        else:
            statistic_end[end_date.month] = 1

    statistic = {}
    for month in range(1, 13):
        if month not in statistic_get.keys():
            statistic_get[month] = 0
        if month not in statistic_end.keys():
            statistic_end[month] = 0
        statistic[month] = [statistic_get[month], statistic_end[month]]
    df = pd.DataFrame.from_dict(statistic,
                                orient='index',
                                columns=['amount of get', 'amount of end'])

    df.index.rename('month', inplace=True)
    print(data)
    print(df.sort_values(by='month'))
    return df.sort_values(by='month')


df = df_month()
df.plot(kind='bar')
plt.show()









