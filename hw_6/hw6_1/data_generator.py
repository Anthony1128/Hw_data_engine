import pandas as pd
import numpy as np
import random


# Generates tuple of random start and end dates
def random_date():
    rd_month = random.randint(1, 12)
    rd_day = random.randint(1, 31)
    rd_hour = random.randint(0, 23)
    rd_minute = random.randint(0, 59)
    start_date = pd.Timestamp(2019, rd_month, rd_day, rd_hour, rd_minute)
    time_delta = pd.Timestamp(2020, 1, 1) - start_date
    n = 10**10
    delta = start_date.value + random.randint(0, time_delta.value/n)*n
    end_date = pd.Timestamp(delta).round(freq='T')
    return start_date.isoformat(), end_date.isoformat()


# Generates random Data Frame
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












