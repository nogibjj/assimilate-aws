#!/usr/bin/env python
"""Build a calcutor command-line tool that adds and subtracts using click package."""

import click

# build an add function
def add(x, y):
    """Add function"""
    return x + y


# build a subtract function
def subtract(x, y):
    """Subtract function"""
    return x - y


# build a click group
@click.group()
def cli():
    """Calculator

    Example:
    $ python cp_calculator.py add 1 2
    3
    """


# build a click command for add
@cli.command("add")
@click.argument("x", type=float)
@click.argument("y", type=float)
def add_cmd(x, y):
    """Add two numbers

    Example:
    $ python cp_calculator.py add 1 2
    """

    result = add(x, y)
    click.echo(result)


# build a click command for subtract
@cli.command("subtract")
@click.argument("x", type=float)
@click.argument("y", type=float)
def subtract_cmd(x, y):
    """Subtract two numbers

    Example:
    $ python cp_calculator.py subtract 1 2
    """

    result = subtract(x, y)
    click.echo(result)


if __name__ == "__main__":
    cli()
