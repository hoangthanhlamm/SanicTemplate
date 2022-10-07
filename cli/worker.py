import click

from app.services.queue.worker import app


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def run_worker():
    """Run worker. """
    argv = [
        'worker',
        '--loglevel=INFO',
    ]
    app.worker_main(argv)
