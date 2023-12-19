import sys

from cloudphoto import config


def delete(album, photo):
    if not album or album == '':
        print(f"Album name can't be empty", file=sys.stderr)
        exit(1)

    s3_client = config.get_client()
    bucket_name = config.get_bucket_name()

    if not config.is_existing_album(s3_client, bucket_name, album):
        print(f"Album {album} doesn't exist", file=sys.stderr)
        exit(1)

    object_name = f"{album}"
    if not (not photo or photo == ''):
        object_name = object_name + "/" + photo

        if not config.is_existing_photo(s3_client, bucket_name, album, photo):
            print(f"Photo {photo} doesn't exist in the {album} album", file=sys.stderr)
            exit(1)

        s3_client.delete_objects(
            Bucket=bucket_name, Delete={"Objects": [{"Key": object_name}]}
        )
    else:
        photo_keys = get_album_photo_keys(s3_client, bucket_name, album)

        s3_client.delete_objects(
            Bucket=bucket_name, Delete={"Objects": photo_keys}
        )


def get_album_photo_keys(client, bucket: str, album: str):
    list_objects = client.list_objects(Bucket=bucket, Prefix=album + '/')["Contents"]
    return [{"Key": photo_key.get('Key')} for photo_key in list_objects]

