import configparser
import os
import sys

import boto3
from botocore.exceptions import ClientError

REGION_VALUE = 'ru-central1'
ENDPOINT_URL_VALUE = 'https://storage.yandexcloud.net'


def get_config_path():
    return os.path.expanduser('~/.config/cloudphoto/cloudphotorc')


def get_default_config():
    config = configparser.ConfigParser()
    config.read(get_config_path())
    return config['DEFAULT']


def read_config():
    config = configparser.ConfigParser()
    config.read(get_config_path())
    return config


def create_config(bucket, aws_access_key_id, aws_secret_access_key):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'bucket': bucket,
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'region': REGION_VALUE,
        'endpoint_url': ENDPOINT_URL_VALUE,
    }
    with open(get_config_path(), mode='w') as f:
        config.write(f)


def is_configured():
    if os.path.exists(get_config_path()):
        config = read_config()
        if config["DEFAULT"]:
            default_config = config["DEFAULT"]
            required_params = ["bucket", "aws_access_key_id", "aws_secret_access_key", "region", "endpoint_url"]
            for param in required_params:
                if param not in default_config or not default_config[param] or default_config[param] == '':
                    return False
            return True

    return False


def get_client():
    session = boto3.session.Session()
    config = get_default_config()

    client = session.client(
        service_name='s3',
        endpoint_url=config['endpoint_url'],
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
    )

    return client


def get_resource():
    session = boto3.session.Session()
    config = get_default_config()

    resource = session.resource(
        service_name='s3',
        endpoint_url=config['endpoint_url'],
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
    )

    return resource


def create_bucket_if_not_exists(bucket_name):
    s3 = get_client()

    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            try:
                s3.create_bucket(Bucket=bucket_name)
            except ClientError as e:
                print(f"Error creating bucket: {e}", file=sys.stderr)
                exit(1)
        else:
            print(f"Error checking bucket existence: {e}", file=sys.stderr)
            exit(1)


def get_bucket_name():
    return get_default_config()['bucket']


def is_existing_album(client, bucket, album):
    list_objects = client.list_objects(Bucket=bucket, Prefix=album + '/')
    if "Contents" in list_objects:
        for _ in list_objects["Contents"]:
            return True

    return False


def is_existing_photo(client, bucket, album, photo):
    try:
        client.get_object(Bucket=bucket, Key=(album + '/' + photo))
    except ClientError as e:
        if e.response["Error"]["Code"] != "NoSuchKey":
            print(f"Error checking photo existence: {e}", file=sys.stderr)
            exit(1)
        return False
    return True
