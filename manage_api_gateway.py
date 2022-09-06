#!/usr/bin/env python
## FYI, this is a command-line tool to manage API Gateways.  In the future, I'll add more functionality to it like delete

import boto3
import click

# write a function that lists all of the api gateways in the account and the date they were created
def list_api_gateways():
    """List all of the api gateways in the account and the date they were created"""
    # create an api gateway client
    apigw = boto3.client("apigateway")
    # get a list of api gateways
    response = apigw.get_rest_apis()
    # loop through the api gateways
    all_gateways = []
    for api in response["items"]:
        # get the name of the api gateway
        api_name = api["name"]
        all_gateways.append(api_name)
        # get the date the api gateway was created
        api_date = api["createdDate"]
        # print the name and date
        print("The api gateway {} was created on {}".format(api_name, api_date))
        # print the total number of api gateways
    print("You have {} api gateways in your account".format(len(response["items"])))
    # return a list of the names of the api gateways
    return all_gateways


# create a click group
@click.group()
def cli():
    """Manage api gateways"""


# add a click command to the cli group
@cli.command("list-api-gateways")
def list_api_gateways_command():
    """List all of the api gateways in the account and the date they were created

    Example:
            ./manage_api_gateway.py list-api-gateways

    """

    gateways = list_api_gateways()
    for gateway in gateways:
        print(gateway)


# run the cli
if __name__ == "__main__":
    cli()
