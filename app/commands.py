import click

from app import pm


@click.command("create_perms")
def create_perms():
    """Create in DB all staged permissions"""
    pm.create_all()
