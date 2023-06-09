import os
import zipfile
import boto3
import argparse
from os import getenv
from my_auto_parser import parse_and_save_to


def upload_files_to_s3(bucket_name, file_path):
    s3_client = boto3.client('s3',
                             aws_access_key_id=getenv("aws_access_key_id"),
                             aws_secret_access_key=getenv("aws_secret_access_key"),
                             aws_session_token=getenv("aws_session_token"),
                             region_name=getenv("aws_region_name"))

    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                print(f"Uploading {file} to s3://{bucket_name}/{file}")
                s3_client.upload_fileobj(zip_ref.open(file), bucket_name, file)
    else:
        for root, dirs, files in os.walk(file_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, file_path)

                print(f"Uploading {local_path} to s3://{bucket_name}/{relative_path}")
                s3_client.upload_file(local_path, bucket_name, relative_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload files to S3 bucket.')
    parser.add_argument('bucket_name', help='Name of the S3 bucket')
    parser.add_argument('local_directory', help='Local directory to upload files from')
    parser.add_argument('--parse', choices=[True, False], default=False, help='Parse site or not')

    args = parser.parse_args()

    if args.parse:
        parse_and_save_to(args.local_directory)

    upload_files_to_s3(args.bucket_name, args.local_directory)
