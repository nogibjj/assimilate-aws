#!/usr/bin/env python

"""
This is a command-line to manage S3 buckets
"""

import boto3
import click


def count_buckets():
    """Count the number of buckets in the account"""
    # create a s3 client
    s3 = boto3.client("s3")
    # get a list of buckets
    response = s3.list_buckets()
    # get the number of buckets
    number_of_buckets = len(response["Buckets"])
    # print the number of buckets
    print("You have {} buckets in your account".format(number_of_buckets))
    return number_of_buckets


# create a function that finds all empty buckets in s3 and returns a list of them as well as a count
def find_empty_buckets():
    """Find all empty buckets in the account"""
    # create a s3 client
    s3 = boto3.client("s3")
    # get a list of buckets
    response = s3.list_buckets()
    # create an empty list to store the names of empty buckets
    empty_buckets = []
    # loop through the buckets
    for bucket in response["Buckets"]:
        # get the name of the bucket
        bucket_name = bucket["Name"]
        # get the number of objects in the bucket
        number_of_objects = len(s3.list_objects(Bucket=bucket_name).get("Contents", []))
        # check if the bucket is empty
        if number_of_objects == 0:
            # add the name of the bucket to the list
            empty_buckets.append(bucket_name)
    return empty_buckets, len(empty_buckets)


def delete_buckets(pattern):
    """Delete all buckets that match a pattern"""
    # create a s3 client
    s3 = boto3.client("s3")
    # get a list of buckets
    response = s3.list_buckets()
    # loop through the buckets
    for bucket in response["Buckets"]:
        # get the name of the bucket
        bucket_name = bucket["Name"]
        # check if the bucket matches the pattern
        if pattern in bucket_name:
            # delete the bucket
            s3.delete_bucket(Bucket=bucket_name)
            print("Deleted bucket {}".format(bucket_name))


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
