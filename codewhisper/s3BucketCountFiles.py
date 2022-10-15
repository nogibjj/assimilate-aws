#!/usr/bin/env python
"""
This is a command-line tool that uses click to count the number of files in all buckets in an aws account
"""
import click
import boto3


def list_buckets():
    """
    This function returns a list of all s3 buckets in an account
    :return: list of s3 bucket names
    """
    s3 = boto3.resource("s3")
    return [bucket.name for bucket in s3.buckets.all()]


def count_files(bucket_name):
    """
    This function returns the number of files in a given s3 bucket
    :param bucket_name: name of s3 bucket
    :return: integer count of files
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    return sum(1 for _ in bucket.objects.all())

#build click group
@click.group()
def cli():
    """
    Example:
        $ python s3BucketCountFiles.py --help
    """
# build a click command for count
@cli.command("count")
def count_cmd():
    """
    This command will print out the number of files in each s3 bucket
    """
    for bucket in list_buckets():
        #use click colors
        click.echo(click.style(f"Bucket: {bucket}", fg="green"))
        click.echo(click.style(f"Files: {count_files(bucket)}", fg="green"))


if __name__ == "__main__":
    cli()
    