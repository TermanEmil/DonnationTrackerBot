import os

import boto3


dynamodb = boto3.resource(
    'dynamodb',
    region_name='eu-central-1',
    aws_access_key_id=os.environ.get('CONFIG_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('CONFIG_AWS_SECRET_ACCESS_KEY'))


def get_db():
    return dynamodb


def get_db_client():
    return boto3.client(
        'dynamodb',
        region_name='eu-central-1',
        aws_access_key_id=os.environ.get('CONFIG_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('CONFIG_AWS_SECRET_ACCESS_KEY'))


def get_s3_client():
    session = boto3.session.Session()
    return session.client(
        's3',
        region_name='eu-central-1',
        aws_access_key_id=os.environ.get('CONFIG_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('CONFIG_AWS_SECRET_ACCESS_KEY'))
