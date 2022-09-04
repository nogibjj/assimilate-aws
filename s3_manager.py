#!/usr/bin/env python

import boto3
import click

# write a function that recursively deletes all objects in a list of buckets
def delete_buckets(buckets):
    s3 = boto3.client("s3")
    print(f"Deleting {len(buckets)} buckets with the following names: {buckets}")
    for bucket in buckets:
        print(f"Deleting bucket {bucket} with full uri s3://{bucket}")
        response = s3.list_objects_v2(Bucket=bucket)
        if "Contents" in response:
            for obj in response["Contents"]:
                s3.delete_object(Bucket=bucket, Key=obj["Key"])
        # after all objects are deleted delete the bucket using ListObjectsV2 to get the bucket name
        s3.delete_bucket(Bucket=bucket)


# write a function that returns a list of buckets that match a pattern
def list_buckets_by_pattern(pattern):
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [
        bucket["Name"] for bucket in response["Buckets"] if pattern in bucket["Name"]
    ]
    return buckets


# write a function that returns all the buckets in s3
def list_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"]]
    return buckets


# write a function that takes a list of buckets and returns a list of buckets that are empty
def list_empty_buckets(buckets):
    s3 = boto3.client("s3")
    empty_buckets = []
    for bucket in buckets:
        response = s3.list_objects_v2(Bucket=bucket)
        if "Contents" not in response:
            empty_buckets.append(bucket)
    return empty_buckets


# write a function that finds s3 buckets last over one year old
def list_old_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [
        bucket["Name"]
        for bucket in response["Buckets"]
        if bucket["CreationDate"].year < 2020
    ]
    return buckets


# add click command
@click.command()
# add click option
@click.option("--empty", is_flag=True, help="Find empty buckets")
# add click option
@click.option("--delete", is_flag=True, help="Delete empty buckets")
# add click option
@click.option("--bucket", help="Name of bucket to delete")
# add click option
@click.option("--pattern", help="Pattern to match in bucket name")
# add click option
@click.option("--old", is_flag=True, help="Find old buckets")
def main(empty, delete, bucket, pattern, old):
    """List and delete S3 buckets

    Examples:
    python s3_manager.py --empty
    python s3_manager.py --delete --bucket my-bucket
    python s3_manager.py --delete --pattern my-bucket

    """
    if old:
        buckets = list_old_buckets()
        print(buckets)
    # delete old buckets
    elif delete and bucket:
        delete_buckets([bucket])
    # if pattern is specified, delete buckets that match the pattern
    if pattern:
        buckets = list_buckets_by_pattern(pattern)
        if delete:
            delete_buckets(buckets)
        else:
            print(buckets)
    # if empty flag is set
    if empty:
        # find empty buckets
        empty_buckets = list_empty_buckets(list_buckets())
        # print empty buckets
        for bucket in empty_buckets:
            # print blue bg with white text
            click.echo(click.style(bucket, bg="white", fg="black", bold=True))
        # if delete flag is set
        if delete:
            # delete empty buckets
            delete_buckets(empty_buckets)
    # if delete flag is set
    if delete:
        # delete bucket and objects in bucket
        delete_buckets([bucket])


# call function via command line
if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
