#!/usr/bin/env python
import pathlib
import boto3
import click
import requests
import json
import openai
import os



#write a functions that summarizes a transcription using the openai api
def summarize_transcription(text):
    """Summarize a transcription"""

    #truncate the text to 4000 characters
    truncate_text = text[:4000]
    openai.api_key = os.getenv("OPENAI_API_KEY")
    full_text_prompt = f"{truncate_text}\n\nTl;dr"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=full_text_prompt,
        max_tokens=256,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text

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


# get the uri of the transcription job to download the transcription
def get_transcription_uri(job_name):
    """Get the uri of a transcription job"""

    transcribe = boto3.client("transcribe")
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    uri_json = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    return uri_json


# download the transcription using requests
def download_transcription(uri_json, filename):
    """Download a transcription"""

    response = requests.get(uri_json, timeout=30)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)


# read the transcription from from a file and return only the text
def read_transcription(filename):
    """Read a transcription"""

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["results"]["transcripts"][0]["transcript"]

# write a function that takes a transcription job name, downloads the transcription, and returns the text
def get_transcription_text(job_name):
    """Get the text of a transcription"""

    uri_json = get_transcription_uri(job_name)
    # print(f"Downloading transcription from {uri_json}")
    filename = f"{job_name}.json"
    print(f"Saving transcription to {filename}")
    download_transcription(uri_json, filename)
    print(f"Transcription downloaded to {filename}")
    text = read_transcription(filename)
    # delete the file
    pathlib.Path(filename).unlink()
    return text

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


@cli.command("get-results")
@click.argument("job_name")
def get_results(job_name):
    """Get the results of a transcription job

    Example: python aws_transcriber.py get-results my-job
    """

    result = get_transcription_text(job_name)
    print(result)

@cli.command("summarize")
@click.argument("job_name")
def summarize(job_name):
    """Summarize a transcription job

    Example: python aws_transcriber.py summarize my-job
    """

    text = get_transcription_text(job_name)
    result = summarize_transcription(text)
    print(result)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
