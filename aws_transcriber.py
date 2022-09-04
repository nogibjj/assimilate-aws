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
    # return a list of transcription job names
    return [obj["Key"] for obj in response["Contents"] if pattern in obj["Key"]]


def list_transcription_jobs():
    """List all transcription jobs"""

    transcribe = boto3.client("transcribe")
    response = transcribe.list_transcription_jobs()
    return response["TranscriptionJobSummaries"]

#write a function that retrieves the transcription job results
def get_transcription_results(job_name):
    """Get the results of a transcription job"""

    transcribe = boto3.client("transcribe")
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    return response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

@click.group()
def cli():
    pass


@cli.command("transcribe")
@click.argument("bucket_name")
def transcribe_all(bucket_name):
    """Transcribe all files in a bucket

    Example: python aws_transcriber.py transcribe my-bucket

    """
    result = transcribe_all_files(bucket_name)
    print(f"Transcribed {len(result)} files")


@cli.command("list-jobs")
def list_jobs():
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
