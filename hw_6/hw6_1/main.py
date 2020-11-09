import pandas as pd
import numpy as np
import requests
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
from hw_6.hw6_1.data_generator import data_generate


# DATA = data_generate(1)
np_ar = np.array([[0, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 1, 18, 0)],
                  [1, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 2, 9, 30)],
                  [2, pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 5, 8, 30)]])
DATA = pd.DataFrame(data=np_ar,
                    columns=['Name', 'Start Date',
                             'End Date']).set_index('Name')


# TODO set year method
class RussianHolidays(AbstractHolidayCalendar):
    url_calendar = 'http://jsoncalendar.ru/data/2020/calendar.json'
    holidays_json = requests.get(url_calendar).json()
    rules = []
    for holiday in holidays_json['days']:
        if holiday['type'] == 1:
            name = holiday['holiday_id']
            month = int(holiday['date_string'][:2])
            day = int(holiday['date_string'][3:])
            rules.append(Holiday(name, month=month, day=day))


def implementation(data):
    for id_r, row in data.iterrows():
        start_date = row[0]
        end_date = row[1]

        delta = pd.Timedelta(days=1)
        if end_date.hour < 8:
            delta = pd.Timedelta(days=0)

        bh = pd.offsets.CustomBusinessHour(start='08:00', end='18:00', calendar=RussianHolidays())
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
        print(row)
        print(hours, minutes)


implementation(DATA)






