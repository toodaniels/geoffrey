import os
import yaml
from yaml.loader import SafeLoader

SPREADER_FOLDER = '.spreader/'


def download_remote_package(package):
    os.system(f'mkdir {SPREADER_FOLDER}')
    os.system(
        f'cd {SPREADER_FOLDER} && git clone {package["host"]}')
    return package.copy() | {"folder": f'{SPREADER_FOLDER}{package["name"]}'}


def up(package):
    os.system(
        f'cd {SPREADER_FOLDER}{package["name"]}/ && docker compose up -d')


def down(package):
    os.system(
        f'cd {SPREADER_FOLDER}{package["name"]}/ && docker compose down')


def get_packages():
    file_yaml = open('packages.yml')
    return yaml.load(file_yaml, Loader=SafeLoader)


def search_package(package_name):
    packages = get_packages()
    if package_name not in packages.keys():
        raise Exception('Package not in packages list')

    return packages[package_name].copy() | {'name': package_name}


def up_package(package_name):
    package = search_package(package_name).copy()

    # Check if the package is remote or local
    if package['type'] == 'remote':
        package = download_remote_package(package)
    up(package)


def down_package(package_name):
    package = search_package(package_name)
    down(package)
