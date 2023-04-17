import subprocess
from rich.console import Console
from rich.table import Table

from packages import get_packages


def search_result(command, search):
    output = subprocess.getoutput(command)
    print(output)
    return search in output


def show_list():

    table = Table(title="Instaled Packages")

    packages = get_packages()

    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Path", justify="right", style="green")

    for package_name, package in packages.items():

        path = package.get('folder') if package.get(
            'folder') else package.get('host')

        table.add_row(package_name, package['type'], path)

    console = Console()
    console.print(table)


if __name__ == "__main__":
    search_result('docker ps', '')
