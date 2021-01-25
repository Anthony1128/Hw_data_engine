from my_package import my_module
import boto3


def lambda_handler(event, context):
    print('starting func')
    s3_client = boto3.client('s3')
    source_bucket = 'de-source-csv-for-lambda'
    object_key = 'netflix_titles.csv'

    dataframe = my_module.read_csv_from_s3(source_bucket, object_key, s3_client)
    print('got the df')
    updated_dataframe = my_module.filter_df(dataframe)
    print(updated_dataframe.head(5))
    my_module.write_df_to_s3('s3://de-sink-csv-for-lambda/de-aws-lambda-from-csv.parquet', updated_dataframe)
    print('DONE!')
