#!/usr/bin/env python
"""Build a command-line tool using click package that counts the number of files in all buckets in an AWS account."""

import click
import boto3


def get_bucket_list():
    """Get a list of all buckets in an AWS account."""
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    return response["Buckets"]


def get_bucket_file_count(bucket_name):
    """Get the number of files in a bucket."""
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name)
    return response["KeyCount"]


# build a click group
@click.group()
def cli():
    """Count the number of files in all buckets in an AWS account.

    Example:
    $ python cp_s3_bucket_file_count.py count
    """


# build a click command for count
@cli.command("count")
def count_cmd():
    """Count the number of files in all buckets in an AWS account.

    Example:
    $ python cp_s3_bucket_file_count.py count
    """

    bucket_list = get_bucket_list()
    for bucket in bucket_list:
        bucket_name = bucket["Name"]
        file_count = get_bucket_file_count(bucket_name)
        # use click colors to print the bucket name and file count
        click.echo(
            click.style(bucket_name, fg="green")
            + ": "
            + click.style(str(file_count), fg="blue")
        )


if __name__ == "__main__":
    cli()
