#!/usr/bin/env python
import boto3
import click


# write a function that list all aws lambda functions created before a certain date
def list_old_lambda_functions(year=2022):
    functions = []
    lambda_client = boto3.client("lambda")
    response = lambda_client.list_functions()
    for function in response["Functions"]:
        lambda_year = function["LastModified"].split("-")[0]
        if int(lambda_year) < year:
            func_name = function["FunctionName"]
            print(f"Found {func_name} created in {lambda_year}")
            functions.append(func_name)
    return functions


# write a function that deletes a list of lambda functions
def delete_lambda_functions(functions):
    lambda_client = boto3.client("lambda")
    print(f"Deleting {len(functions)} functions with the following names: {functions}")
    for function in functions:
        print(f"Deleting function {function}")
        response = lambda_client.delete_function(FunctionName=function)
        print(f"Response: {response}")
    return response


@click.command()
# add option to list old lambda functions
@click.option(
    "--list-lambda", is_flag=True, help="List all lambda functions over 1 year old"
)
# add an option to delete the old functions
@click.option("--delete", is_flag=True, help="Delete old lambda functions")
# add an option to delete the old functions earlier than year
@click.option(
    "--year", default=2020, help="Delete old lambda functions earlier than year"
)
def main(delete, list_lambda, year):
    if list_lambda:
        print(list_old_lambda_functions())
    if delete:
        functions = list_old_lambda_functions(year)
        delete_lambda_functions(functions)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
