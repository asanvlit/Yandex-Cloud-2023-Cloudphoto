import sys
from pathlib import Path

from cloudphoto import config


def list_album_photos(album):
    s3_resource = config.get_resource()
    s3_client = config.get_client()

    bucket_name = config.get_bucket_name()

    if not album or album == '':
        list_objects = s3_client.list_objects(Bucket=bucket_name)
        albums = set()
        if "Contents" in list_objects:
            for key in list_objects["Contents"]:
                if key["Key"].endswith('/'):
                    albums.add(Path(key["Key"]))
                elif "/" in key["Key"]:
                    albums.add(Path(key["Key"]).parent)

        if len(albums) == 0:
            print(f"The bucket '{bucket_name}' doesn't contain albums", file=sys.stderr)
            exit(1)

        for album in albums:
            print(album)
    else:
        objects = s3_resource.Bucket(config.get_bucket_name()).objects.filter(Prefix=album + '/')
        objects = [obj for obj in objects if not obj.key.endswith('/')]
        if len(objects) == 0:
            print(f"Album {album} doesn't contain photos or doesn't exist", file=sys.stderr)
            exit(1)
        for obj in objects:
            print(obj.key.split('/')[-1])
