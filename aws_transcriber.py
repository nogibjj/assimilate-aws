#!/usr/bin/env python

import click
from awstools.transcribelib import (
    summarize_transcription,
    transcribe_all_files,
    list_transcription_jobs,
    get_transcription_text,
)


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
