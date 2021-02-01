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