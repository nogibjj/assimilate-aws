#!/usr/bin/env python

"""
This is a command-line to manage S3 buckets
"""
import click
from awstools.s3lib import count_buckets, find_empty_buckets, delete_buckets


@click.group()
def cli():
    """Manage S3 buckets"""


# create a command that finds all empty buckets in s3 and returns a list of them
@cli.command("find-empty-buckets")
def find_empty_buckets_command():
    """Find all empty buckets in the account

    Example: ./manage_s3_tools.py find-empty-buckets
    """
    # print a count of the empty buckets and the names of the empty buckets
    print("You have {} empty buckets in your account: {}".format(*find_empty_buckets()))
    # print all the empty buckets line by line
    for bucket in find_empty_buckets()[0]:
        print(bucket)


# create a sub-command that delete buckets that match a pattern
@cli.command("delete-buckets")
@click.argument("pattern")
def delete_buckets_command(pattern):
    """Delete all buckets that match a pattern

    Example: ./manage_s3_tools.py delete-buckets test
    """
    # delete all buckets that match the pattern
    delete_buckets(pattern)


# create a click subcommand
@cli.command("count")
def count():
    """Count the number of buckets in the account

    Example: ./manage_s3_tools.py count

    The above command will print the number of buckets in the account
    like this:

    You have 2 buckets in your account
    """
    count_buckets()


if __name__ == "__main__":
    cli()
