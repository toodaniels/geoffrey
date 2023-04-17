import click
from packages import up_package, down_package, get_packages
from console import show_list


@click.group()
def cli():
    pass


@click.command()
@click.argument('package')
def up(package):
    click.echo(f'Starting {package}')
    up_package(package)


@click.command()
@click.argument('package')
def down(package):
    click.echo(f'Stopping {package}')
    down_package(package)


@click.command(name='list')
def list_():
    show_list()


cli.add_command(up)
cli.add_command(down)
cli.add_command(list_)


if __name__ == '__main__':
    cli()
