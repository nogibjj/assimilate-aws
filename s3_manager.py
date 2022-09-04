#!/usr/bin/env python

import boto3
import click

#write a function that returns all the buckets in s3
def list_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"]]
    return buckets

#write a function that takes a list of buckets and returns a list of buckets that are empty
def list_empty_buckets(buckets):
    s3 = boto3.client("s3")
    empty_buckets = []
    for bucket in buckets:
        response = s3.list_objects_v2(Bucket=bucket)
        if "Contents" not in response:
            empty_buckets.append(bucket)
    return empty_buckets

# add click command
@click.command()
# add click option
@click.option("--empty", is_flag=True, help="Find empty buckets")
# add click option
@click.option("--delete", is_flag=True, help="Delete empty buckets")
# add click option
@click.option("--bucket", help="Name of bucket to delete")
def main(empty, delete, bucket):
    # if empty flag is set
    if empty:
        # find empty buckets
        empty_buckets = list_empty_buckets(list_buckets())
        # print empty buckets
        for bucket in empty_buckets:
            #print green text
            click.style(click.echo(bucket), fg="orange")
    # if delete flag is set
    if delete:
        # create s3 client
        s3 = boto3.client("s3")
        # delete bucket
        s3.delete_bucket(Bucket=bucket)


# call function via command line
if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
