#!/usr/bin/env python

import boto3
import click

#write a function that takes a list of buckets and deletes all of the contents of each bucket and then deletes the bucket
def delete_buckets(buckets):
    """Delete all the contents of a list of buckets and then delete the buckets"""

    s3 = boto3.client("s3")
    for bucket in buckets:
        print(f"Deleting bucket {bucket} and all of its contents")
        response = s3.list_objects_v2(Bucket=bucket)
        if "Contents" in response:
            objects = [object["Key"] for object in response["Contents"]]
            s3.delete_objects(Bucket=bucket, Delete={"Objects": [{"Key": object} for object in objects]})
        s3.delete_bucket(Bucket=bucket)


#write a function that returns a list of buckets that match a pattern
def list_buckets_by_pattern(pattern):
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"] if pattern in bucket["Name"]]
    return buckets

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
# add click option
@click.option("--pattern", help="Pattern to match in bucket name")
def main(empty, delete, bucket, pattern):
    """List and delete S3 buckets
    
    Examples:
    python s3_manager.py --empty
    python s3_manager.py --delete --bucket my-bucket
    python s3_manager.py --delete --pattern my-bucket
    
    """
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
