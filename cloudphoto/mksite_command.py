import sys

from botocore.exceptions import ClientError
from jinja2 import Template

from cloudphoto import config, templates

WEBSITE_CONFIG = {
    "ErrorDocument": {"Key": "error.html"},
    "IndexDocument": {"Suffix": "index.html"},
}
TEMP_TEMPLATES_DIR = "temp"


def get_album_photos(client, bucket: str):
    albums = {}
    list_objects = client.list_objects(Bucket=bucket)
    for key in list_objects["Contents"]:
        album_img = key["Key"].split("/", 1)
        if len(album_img) < 2:
            continue
        album, img = album_img
        if album in albums:
            albums[album].append(img)
        else:
            albums[album] = [img]

    return albums


def get_url(bucket_name):
    return f"http://{bucket_name}.website.yandexcloud.net"


def mk_site():
    s3_client = config.get_client()
    s3_resource = config.get_resource()

    bucket_name = config.get_bucket_name()

    album_photos = get_album_photos(s3_client, bucket_name)
    processed_albums = []

    i = 1
    for album, photos in album_photos.items():
        template_name = f"album{i}.html"
        cur_album = Template(templates.album_template).render(album=album, images=photos, url=get_url(bucket_name))
        s3_client.put_object(Bucket=bucket_name, Key=f'album{i}.html', Body=cur_album)

        processed_albums.append({"name": template_name, "album": album})
        i += 1

    rendered_index = Template(templates.index_template).render(template_objects=processed_albums)
    s3_client.put_object(Bucket=bucket_name, Key='index.html', Body=rendered_index)

    s3_client.put_object(Bucket=bucket_name, Key='error.html', Body=templates.error_template)

    try:
        s3_client.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=WEBSITE_CONFIG)
        s3_resource.BucketAcl(bucket_name).put(ACL='public-read')
    except ClientError as e:
        print(f"An error occurred when trying to open the website: {e}", file=sys.stderr)
        exit(1)
