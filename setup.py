import pathlib

from setuptools import setup, find_packages
from io import open
from os import path


HERE = pathlib.Path(__file__).parent

README_TEXT = (HERE / "README.md").read_text()

with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup(
    name='cloudphoto',
    description='A command-line application (CLI) for managing albums, photos in Yandex Object Storage cloud storage, '
                'for generating and publishing photo archive web pages.',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        cloudphoto=cloudphoto.main:main
    ''',
    author="Angelina Savincheva 11-001",
    long_description=README_TEXT,
    long_description_content_type="text/markdown",
    url='https://github.com/asanvlit/Yandex-Cloud-2023-Cloudphoto',
    dependency_links=dependency_links,
    author_email='inf1angelina@gmail.com'
)
