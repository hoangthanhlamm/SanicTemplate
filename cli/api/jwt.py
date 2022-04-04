import click

from app.utils.jwt_utils import generate_jwt


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def generate_jwt_cli():
    """Generate jwt for authorize api. """
    token = generate_jwt()
    print(token)
