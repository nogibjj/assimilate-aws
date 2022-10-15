#!/usr/bin/env python

"""
build a command-line calculator that adds and subtracts integers
and uses python click library
"""

import click


def addit(x, y):
    return x + y


def subit(x, y):
    return x - y


@click.group()
def cli():
    """Calculator"""


@cli.command("add")
@click.option("--x", type=click.INT, help="first number")
@click.option("--y", type=click.INT, help="second number")
def add(x, y):
    """
    This is calculator function

    Example:
        ./calculator add --x 5 --y 6

    """
    click.echo(addit(x, y))


@cli.command("subtract")
@click.option("--x", type=click.INT, help="first number")
@click.option("--y", type=click.INT, help="second number")
def subtract(x, y):
    """
    This is calculator function

    Example:
        ./calculator subtract --x 5 --y 6

    """
    click.echo(subit(x, y))


if __name__ == "__main__":
    cli()
