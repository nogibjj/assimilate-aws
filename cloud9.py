#!/usr/bin/env python

import boto3
import click

# build a function that lists all cloud9 environments
def list_cloud9():
    """List all cloud9 environments"""
    # create a client object
    client = boto3.client("cloud9")
    # get a list of all cloud9 environments
    response = client.list_environments()
    # return the list of cloud9 environments
    return response["environmentIds"]


# build a function that describes a cloud9 environment
def describe_cloud9(environment_id):
    """Describe a cloud9 environment"""
    # create a client object
    client = boto3.client("cloud9")
    # get a list of all cloud9 environments
    response = client.describe_environments(environmentIds=[environment_id])
    # return the list of cloud9 environments
    return response["environments"][0]


# build out click group
@click.group()
def cli():
    """A simple command line interface for AWS Cloud9"""


@cli.command("list")
def cli_list_cloud9():
    """List all cloud9 environments"""
    # get a list of all cloud9 environments
    environments = list_cloud9()
    # print the list of cloud9 environments
    for environment in environments:
        # print using click colors
        click.secho(environment, fg="blue")


@cli.command("describe")
@click.argument("environment_id")
def cli_describe_cloud9(environment_id):
    """Describe a cloud9 environment"""
    # get a list of all cloud9 environments
    environment = describe_cloud9(environment_id)
    # print the list of cloud9 environments
    click.secho("Name: {}".format(environment["name"]), fg="blue")
    click.secho("ID: {}".format(environment["id"]), fg="yellow")
    click.secho("Description: {}".format(environment["description"]), fg="white")


# run the cli
if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
