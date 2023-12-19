import os
import sys
from pathlib import Path

from cloudphoto import config


def download(album, path):
    if not album or album == '':
        print(f"Album name can't be empty", file=sys.stderr)
        exit(1)
    if not os.path.exists(path) or not Path(path).is_dir():
        print(f'Directory {path} not found', file=sys.stderr)
        exit(1)

    s3_resource = config.get_resource()
    s3_client = config.get_client()

    objects = s3_resource.Bucket(config.get_bucket_name()).objects.filter(Prefix=album + '/')
    if len([obj for obj in objects]) == 0:
        print(f"Album {album} doesn't exist", file=sys.stderr)
        exit(1)

    for obj in objects:
        if obj.key.lower().endswith(('.jpg', '.jpeg')):
            file_name = obj.key.split('/')[-1]
            s3_client.download_file(config.get_bucket_name(), obj.key, os.path.join(path, file_name))
