import boto3


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
