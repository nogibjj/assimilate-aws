#!/usr/bin/env python


import boto3
import click


def transcribe_all_files(bucket_name, pattern="mp4"):
    """Transcribe all files in a bucket"""

    s3 = boto3.client("s3")
    transcribe = boto3.client("transcribe")
    response = s3.list_objects_v2(Bucket=bucket_name)
    for obj in response["Contents"]:
        if pattern in obj["Key"]:
            job_uri = f"s3://{bucket_name}/{obj['Key']}"
            print(f"Transcribing {job_uri}")
            key = obj["Key"]
            print(f"Transcribing {key}")
            response = transcribe.start_transcription_job(
                TranscriptionJobName=key,
                Media={"MediaFileUri": f"s3://{bucket_name}/{key}"},
                MediaFormat="mp4",
                LanguageCode="en-US",
            )
        print(f"Response: {response}")
    #return a list of transcription job names
    return [obj["Key"] for obj in response["Contents"] if pattern in obj["Key"]]

#write a function that lists all the transcription jobs
def list_transcription_jobs():
    transcribe = boto3.client("transcribe")
    response = transcribe.list_transcription_jobs()
    return response["TranscriptionJobSummaries"]

@click.group()
def cli():
    pass

@cli.command("transcribe")
@click.argument("bucket_name")
def transcribe(bucket_name):
    """Transcribe all files in a bucket
    
    Example: python aws_transcriber.py transcribe my-bucket

    """
    result = transcribe_all_files(bucket_name)
    print(f"Transcribed {len(result)} files")

@cli.command("list")
def list():
    """List all transcription jobs
    
    Example: python aws_transcriber.py list
    """

    result = list_transcription_jobs()
    print(f"Found {len(result)} jobs")
    for job in result:
        print(job["TranscriptionJobName"])

    
    


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()



