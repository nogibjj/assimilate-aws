#!/usr/bin/env python

import openai
import os
import click
import urllib.request
from bs4 import BeautifulSoup


def extract_from_url(url):
    text = ""
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        },
    )
    html = urllib.request.urlopen(req)
    parser = BeautifulSoup(html, "html.parser")
    for paragraph in parser.find_all("p"):
        print(paragraph.text)
        text += paragraph.text

    # return a max of 1500 characters
    return text[:1500]


# write an openai function that summarizes the text
def summarize(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # create a tl;dr prompt
    prompt = f"{text}\n\nTl;dr"

    result = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-002",
    )["choices"][0]["text"].strip(" \n")
    return result


def submit_question(text):
    """This submits a question to the OpenAI API"""

    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text

    result = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-002",
    )["choices"][0]["text"].strip(" \n")
    return result


# build a click group
@click.group()
def cli():
    """An OpenAI tool to answer questions"""


# build a click command that takes a question
@cli.command("question")
@click.argument("text")
def question(text):
    """This is the main function that you ask the OpenAI API a question to get an answer

    example: ./openaiAnswerbotCli.py question "Who won the 2020 Summer Olympics?"

    """
    print(submit_question(text))


# build a click command that takes a url and summarizes it
@cli.command("summarize")
@click.argument("url")
def summarize_url(url):
    """This is the main function that you ask the OpenAI API a question to get an answer

    example: ./openaiAnswerbotCli.py summarize "https://en.wikipedia.org/wiki/2020_Summer_Olympics"

    """
    print(summarize(extract_from_url(url)))


# run the cli
if __name__ == "__main__":
    cli()
