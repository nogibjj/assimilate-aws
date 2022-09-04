import boto3

# build function to upload mp4 to s3 and transcribe
def transcribe_mp4(filename):
    # create s3 client
    s3 = boto3.client("s3")
    # upload file to s3
    s3.upload_file(filename, "my-bucket", filename)
    # create transcribe client
    #transcribe = boto3.client("transcribe")
    # start transcription job
    #transcribe.start_transcription_job
