import boto3
import click


def list_empty_buckets():
    """List all empty buckets in your account"""

    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"]]
    empty_buckets = []
    for bucket in buckets:
        response = s3.list_objects_v2(Bucket=bucket)
        if "Contents" not in response:
            empty_buckets.append(bucket)
    return empty_buckets


# build a click app that lists all empty buckets
@click.command("empty")
def list_empty_buckets_cli():
    """List all empty buckets in your account

    Example: s3tool empty
    """

    empty_buckets = list_empty_buckets()
    for bucket in empty_buckets:
        print(bucket)


if __name__ == "__main__":
    list_empty_buckets_cli()
