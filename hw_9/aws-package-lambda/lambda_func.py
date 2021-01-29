from my_package import my_module
import boto3
from time import time


def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    source_bucket = 'de-source-csv-for-lambda'
    sink_bucket = 'de-sink-csv-for-lambda'

    object_key = 'netflix_titles.csv'
    dataframe = my_module.read_csv_from_s3(source_bucket, object_key, s3_client)
    print('\n----------origin df----------')
    print(dataframe.head(5))

    updated_dataframe = my_module.filter_df(dataframe)
    print('\n----------updated df----------')
    print(updated_dataframe.head(5))

    parquet_object_name = f'de-aws-from-csv-{time()}'
    my_module.write_df_to_s3(f's3://{sink_bucket}/{parquet_object_name}.parquet', updated_dataframe)
    print('\nparquet written to s3')

    print('sending to sql')
    df = my_module.write_df_to_db("de-aws-rds-postgres.ctbespkpmdex.eu-central-1.rds.amazonaws.com:5432", updated_dataframe)
    print('\n----------read df from sql----------')
    print(df.head(5))
    return 'DONE!'
