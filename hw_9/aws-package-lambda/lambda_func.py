from my_package import my_module
import boto3
from time import time


def lambda_handler(event, context):
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')
    source_bucket = 'de-source-csv-for-lambda'
    sink_bucket = 'de-sink-csv-for-lambda'

    object_keys = []
    for s3_object in s3_resource.Bucket(source_bucket).objects.all():
        if str(s3_object.key)[-3:] == 'csv':
            object_key = str(s3_object.key)
            object_keys.append(object_key)

    for object_key in object_keys:
        dataframe = my_module.read_csv_from_s3(source_bucket, object_key, s3_client)
        print('\n----------origin df (sample)----------')
        print(dataframe.head(5))

        updated_dataframe = my_module.filter_df(dataframe)
        print('\n----------updated df (sample)----------')
        print(updated_dataframe.head(5))

        parquet_object_name = f'de-aws-from-csv-{object_key[:-4]}'
        my_module.write_df_to_s3(f's3://{sink_bucket}/{parquet_object_name}.parquet', updated_dataframe)
        print('\nparquet written to s3')

        print('sending to sql')
        table_name = f'table_{object_key[:-4]}'
        df = my_module.write_df_to_db("de-aws-rds-postgres.ctbespkpmdex.eu-central-1.rds.amazonaws.com:5432", updated_dataframe, table_name)
        print('\n----------read df from sql (sample)----------')
        print(df.head(5))
    return 'DONE!'
