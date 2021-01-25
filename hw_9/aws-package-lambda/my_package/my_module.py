import pandas as pd
import awswrangler as wr
from io import StringIO


def read_csv_from_s3(s3_bucket_name, object_key,  client):
    s3_object = client.get_object(Bucket=s3_bucket_name, Key=object_key)
    data = s3_object['Body'].read().decode('utf-8')
    dataframe = pd.read_csv(StringIO(data))
    return dataframe


def filter_df(dataframe):
    columns_to_select = set(dataframe.columns[:len(dataframe.columns) // 2])
    for column, type in dict(dataframe.dtypes).items():
        if column in ['country']:
            columns_to_select.add(column)
            country = dataframe.sample()['country']
    df = dataframe[columns_to_select][dataframe['country'] == country.item()] \
        if not country.empty else dataframe[columns_to_select]

    values = {column: -1 if type in ['int', 'float'] else 'empty' for
              column, type in dict(dataframe.dtypes).items()}
    updated_df = df.fillna(value=values)

    return updated_df


def write_df_to_s3(s3_bucket_name, dataframe):
    wr.s3.to_parquet(df=dataframe, path=s3_bucket_name)


def write_df_to_db():
    pass
