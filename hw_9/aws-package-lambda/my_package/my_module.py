import pandas as pd
from sqlalchemy import create_engine
import awswrangler as wr
from time import time
from io import StringIO
import rds_config


def read_csv_from_s3(s3_bucket_name, object_key,  client):
    s3_object = client.get_object(Bucket=s3_bucket_name, Key=object_key)
    data = s3_object['Body'].read().decode('utf-8')
    dataframe = pd.read_csv(StringIO(data))
    return dataframe


def filter_df(dataframe):
    columns_to_select = set(dataframe.columns[:len(dataframe.columns) // 2])
    country = pd.DataFrame([{}])
    column_country = ''
    for column, type in dict(dataframe.dtypes).items():
        if 'country' in str(column).lower():
            columns_to_select.add(column)
            column_country = str(column)
            country = dataframe.sample()[column_country]
    df = dataframe[columns_to_select][dataframe[column_country] == country.item()] \
        if not country.empty else dataframe[columns_to_select]

    values = {column: -1 if type in ['int', 'float'] else 'empty' for
              column, type in dict(dataframe.dtypes).items()}
    updated_df = df.fillna(value=values)

    return updated_df


def write_df_to_s3(s3_bucket_name, dataframe):
    wr.s3.to_parquet(df=dataframe, path=s3_bucket_name)


def write_df_to_db(rds_host, dataframe, table_name):
    user = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    engine = create_engine(f'postgresql://{user}:{password}@{rds_host}/{db_name}')
    df = dataframe
    df.to_sql(name=f'{table_name}', con=engine, if_exists='replace', index=False)
    df = pd.read_sql_table(table_name=table_name, con=engine)
    return df
