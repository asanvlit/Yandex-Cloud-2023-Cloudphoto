import argparse
import sys

from cloudphoto import init_command, upload_command, config, download_command, list_command, delete_command, \
    mksite_command


def main():
    parser = argparse.ArgumentParser(description='cloudphoto')
    parser.add_argument('command')
    parser.add_argument('--album', default=None)
    parser.add_argument('--photo')
    parser.add_argument('--path', default='.')
    args = parser.parse_args()

    match args.command:
        case 'init':
            init_command.init()
        case 'upload':
            validate_config()
            upload_command.upload(args.album, args.path)
        case 'download':
            validate_config()
            download_command.download(args.album, args.path)
        case 'list':
            validate_config()
            list_command.list_album_photos(args.album)
        case 'delete':
            validate_config()
            delete_command.delete(args.album, args.photo)
        case 'mksite':
            validate_config()
            mksite_command.mk_site()
        case _:
            print(f'Unknown command: "{args.command}"', file=sys.stderr)
            exit(1)


def validate_config():
    if not config.is_configured():
        print('Not configured. Please run `init`', file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
