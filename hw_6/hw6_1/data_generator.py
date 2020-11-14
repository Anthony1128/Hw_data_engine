import pandas as pd
import numpy as np
import random


# Generates tuple of random start and end dates
def random_date():
    rd_month = random.randint(1, 12)
    if rd_month in [1, 3, 5, 7, 8, 10, 12]:
        rd_day = random.randint(1, 31)
    elif rd_month == 2:
        rd_day = random.randint(1, 28)
    else:
        rd_day = random.randint(1, 30)
    rd_hour = random.randint(0, 23)
    rd_minute = random.randint(0, 59)
    start_date = pd.Timestamp(2019, rd_month, rd_day, rd_hour, rd_minute)
    time_delta = pd.Timestamp(2020, 1, 1) - start_date
    delta = start_date.value + random.randint(0,
                                              time_delta.value/10**10)*10**10
    end_date = pd.Timestamp(delta).round(freq='T')
    # return start_date.isoformat(), end_date.isoformat()
    return start_date, end_date


# Generates random Data Frame with n rows
def data_generate(n):
    data_array = []
    for i in range(n):
        dates = random_date()
        data_array.append([i, dates[0], dates[1]])
    np_array = np.array(data_array)
    df = pd.DataFrame(data=np_array,
                      columns=['Name', 'Start Date',
                               'End Date']).set_index('Name')
    return df












