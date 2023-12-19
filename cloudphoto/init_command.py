from cloudphoto import config


def get_input(prompt, message):
    value = input(prompt)
    while value == '':
        print(message)
        value = input(prompt)
    return value


def init():
    bucket = get_input('Please enter the name of the bucket: ', "Bucket name can't be empty. ")
    aws_access_key_id = get_input('Please enter the aws_access_key_id value: ',
                                  "aws_access_key_id value can't be empty. ")
    aws_secret_access_key = get_input('Please enter the aws_secret_access_key value: ',
                                      "aws_secret_access_key value can't be empty. ")

    config.create_config(bucket, aws_access_key_id, aws_secret_access_key)

    config.create_bucket_if_not_exists(bucket)
