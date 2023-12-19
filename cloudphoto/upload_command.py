import os
import sys
from pathlib import Path

from cloudphoto import config


def upload(album, path):
    if not album or album == '':
        print(f"Album name can't be empty", file=sys.stderr)
        exit(1)
    if not os.path.exists(path) or not Path(path).is_dir():
        print(f'Directory {path} not found', file=sys.stderr)
        exit(1)

    s3 = config.get_client()

    uploaded_count = 0
    for f in os.listdir(path):
        if not (f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')):
            continue
        uploaded_count += 1
        object_name = f"{album}/{f}"
        try:
            s3.upload_file(os.path.join(path, f), config.get_bucket_name(), object_name)
        except Exception as e:
            print(f"Failed to upload {f} file: {e}", file=sys.stderr)

    if uploaded_count == 0:
        print(f"The directory {path} doesn't contain images", file=sys.stderr)
        exit(1)
