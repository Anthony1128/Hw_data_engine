import pytest
import pandas as pd
from main import get_implementation_time


# passing different params to the 'get_implementation_time' function
@pytest.mark.parametrize(
    'start_date, end_date, expected_result',
    [
        (pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 1, 18, 0),
         pd.Timedelta('0 days 00:00:00')),
        (pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 2, 9, 30),
         pd.Timedelta('0 days 01:30:00')),
        (pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 5, 19, 0),
         pd.Timedelta('1 days 06:00:00')),
        (pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 12, 5, 8, 30),
         pd.Timedelta('10 days 0:00:00')),
        (pd.Timestamp(2020, 1, 2, 8, 0), pd.Timestamp(2020, 1, 10, 10, 0),
         pd.Timedelta('0 days 12:00:00')),
        (pd.Timestamp(2020, 11, 1, 8, 0), pd.Timestamp(2020, 11, 1, 8, 0),
         pd.Timedelta('0 days 00:00:00'))
    ]
)
def test_create_dict_timedelta(start_date, end_date, expected_result):
    count_dates_dict = {i: [0, 0] for i in range(1, 13)}
    # start tests with set above parameters
    assert get_implementation_time(start_date, end_date,
                                   count_dates_dict) == expected_result









