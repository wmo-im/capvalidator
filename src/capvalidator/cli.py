import click
from capvalidator import __version__, validate_cap, check_schema, check_integrity, check_signature # noqa


@click.group()
@click.version_option(version=__version__)
def cli():
    """CAP Validator tool"""

    pass


cli.add_command(validate_cap)
cli.add_command(check_schema)
cli.add_command(check_integrity)
cli.add_command(check_signature)
