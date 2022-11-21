#!/usr/bin/env python
"""Sync a directory to s3 using subprocess

"""
import subprocess
import click

#def build a function to sync a directory to s3 using subprocess and aws sync
def sync_to_s3(source, bucket):
    """Sync a directory to s3 using subprocess

    """
    subprocess.run(["aws", "s3", "sync", source, bucket])

@click.group(
    help="Sync a directory to s3 using subprocess"
)
def cli():
    """Sync a directory to s3 using subprocess

    """

@cli.command("sync")
@click.argument("source", default="test-sync-dir")
@click.argument("bucket", default="s3://programatic-sync-test-11-21")
def sync(source, bucket):
    """Sync a directory to s3 using subprocess

    """
    sync_to_s3(source, bucket)


if __name__ == "__main__":
    cli()

