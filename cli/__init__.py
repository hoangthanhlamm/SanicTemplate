import click

from cli.api.refresh_cache import refresh_cache
from cli.api.jwt import generate_jwt_cli


@click.group()
@click.version_option(version='1.6.3')
@click.pass_context
def cli(ctx):
    pass


cli.add_command(refresh_cache, "refresh_cache")
cli.add_command(generate_jwt_cli, "generate_jwt")
