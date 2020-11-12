import pytest
import pandas as pd
import numpy as np
from main import get_implementation_time, RussianHolidays


# TODO warnings
@pytest.mark.parametrize(
    'row_of_df, expected_result',
    [
        (np.array([[0, pd.Timestamp(2020, 11, 1, 8, 0),
                    pd.Timestamp(2020, 11, 1, 18, 0)]]),
            {0: pd.Timedelta('0 days 00:00:00')}),
        (np.array([[1, pd.Timestamp(2020, 11, 1, 8, 0),
                    pd.Timestamp(2020, 11, 2, 9, 30)]]),
            {1: pd.Timedelta('0 days 01:30:00')}),
        (np.array([[2, pd.Timestamp(2020, 11, 1, 8, 0),
                    pd.Timestamp(2020, 11, 5, 19, 0)]]),
            {2: pd.Timedelta('1 days 06:00:00')}),
        (np.array([[3, pd.Timestamp(2020, 11, 1, 8, 0),
                    pd.Timestamp(2020, 12, 5, 8, 30)]]),
            {3: pd.Timedelta('9 days 14:30:00')}),
        (np.array([[5, pd.Timestamp(2020, 1, 2, 8, 0),
                    pd.Timestamp(2020, 1, 10, 10, 0)]]),
            {5: pd.Timedelta('0 days 12:00:00')}),
        (np.array([[4, pd.Timestamp(2020, 11, 1, 8, 0),
                    pd.Timestamp(2020, 11, 1, 10, 0)]]),
            {4: pd.Timedelta('0 days 00:00:00')})
    ]
)
def test_get_implementation_time(row_of_df, expected_result):
    rus_cal = RussianHolidays()
    DATA = pd.DataFrame(data=row_of_df,
                        columns=['Name',
                                 'Start Date', 'End Date']).set_index('Name')
    assert get_implementation_time(DATA, rus_cal) == expected_result









