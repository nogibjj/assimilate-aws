#!/usr/bin/env python

from awstools.translatelib import translate_text, list_languages
import click
from random import choices


# build out click group
@click.group()
def cli():
    """A simple command line interface for AWS Translate"""


# build out click command to list languages
@cli.command("languages")
def cli_list_languages():
    """List available languages"""

    colors = ["red", "green", "blue", "yellow", "magenta", "cyan", "white"]
    languages = list_languages()
    for language in languages:
        # randomly select a color
        color = choices(colors)
        # print the language name in the randomly selected color
        result = f"{language['LanguageName']}, {language['LanguageCode']}"
        click.secho(result, fg=color[0])


@cli.command("translate")
@click.argument("text")
@click.option("--source", default="en", help="Source language")
@click.option("--target", default="es", help="Target language")
def translate(text, source, target):
    """Translate text from source to target language

    Example:
    ./translator_cli.py translate "Hello World" --source en --target es

    """

    text, source, target = translate_text(text, source, target)
    # use colored text to highlight the source and target languages
    click.secho("Source: {}".format(source), fg="blue")
    click.secho("Target: {}".format(target), fg="yellow")
    click.secho(text, fg="white")


# run the cli
if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
