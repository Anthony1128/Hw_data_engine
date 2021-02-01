terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
  profile = "default"
}

// ----- IAM settings -----
resource "aws_iam_policy" "lambda_policy_s3" {
  name        = "lambda_policy_s3"
  path        = "/"
  description = "policy for s3 - full"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "s3:*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_iam_attach" {
  policy_arn = aws_iam_policy.lambda_policy_s3.arn
  role = aws_iam_role.iam_for_lambda.name
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aws-de-lambda-func-tf.arn
  principal     = "s3.amazonaws.com"
  source_arn    = data.aws_s3_bucket.bucket.arn
}

// ----- Deploying lambda function -----
locals {
  my_function_source = "zip_package/aws_package_lambda_tf.zip"
}

data "archive_file" "lambda_func" {
  output_path = local.my_function_source
  type = "zip"
  source_dir = "../aws-package-lambda"
}

resource "aws_s3_bucket_object" "lambda_zip_s3" {
  bucket = "de-lambda-package-zip"
  key    = "aws_package_lambda_tf.zip"
  source = data.archive_file.lambda_func.output_path
  etag = filebase64sha256(data.archive_file.lambda_func.output_path)
  depends_on = [data.archive_file.lambda_func]
}

resource "aws_lambda_function" "aws-de-lambda-func-tf" {
  s3_bucket = "de-lambda-package-zip"
  s3_key    = "aws_package_lambda_tf.zip"
  function_name = "aws-de-lambda-func-tf"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_func.lambda_handler"
  memory_size = 256
  timeout = 20

  source_code_hash = data.archive_file.lambda_func.output_base64sha256
  depends_on = [aws_s3_bucket_object.lambda_zip_s3]
  runtime = "python3.8"
}

// ----- Adding CloudWatch trigger -----
resource "aws_cloudwatch_event_rule" "every_day_at_time" {
  name = "every_day_at_time"
  description = "every_day_at_time"
  schedule_expression = "cron(00 13 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "check_func" {
  rule = aws_cloudwatch_event_rule.every_day_at_time.name
  target_id = "aws-de-lambda-func-tf"
  arn = aws_lambda_function.aws-de-lambda-func-tf.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_func" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aws-de-lambda-func-tf.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.every_day_at_time.arn
}

// ----- Adding S3 trigger -----
data "aws_s3_bucket" "bucket" {
  bucket = "de-source-csv-for-lambda"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = data.aws_s3_bucket.bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.aws-de-lambda-func-tf.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}
