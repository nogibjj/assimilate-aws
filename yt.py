#!/usr/bin/env python
from pyyoutube import Api
import os
import click


API = Api(api_key=os.environ["API_KEY"])
CHANNEL = os.environ["YT_CHANNEL"]


def get_channel_info(channel_id, api=API):
    """Get channel info"""
    channel_info = api.get_channel_info(channel_id=channel_id)
    return channel_info.items[0]


def get_channel_playlist(channel_id, api=API):
    """Get channel's playlist"""
    playlists_by_channel = api.get_playlists(channel_id=channel_id, count=None)
    return playlists_by_channel.items


def get_playlist_name(playlist_id, api=API):
    """Get playlist name"""
    playlist_info = api.get_playlist_info(playlist_id=playlist_id)
    return playlist_info.items[0].snippet.title


@click.group()
def cli():
    pass


@cli.command("channel")
@click.option("--channel-id", default=CHANNEL, help="Channel ID")
def cli_channel_info(channel_id):
    """Get channel info
    Example: yt channel --channel-id <your key>
    """

    channel = get_channel_info(channel_id)
    print(channel)


@cli.command("playlists")
@click.option("--channel-id", default=CHANNEL, help="Channel ID")
def list_playlists(channel_id):
    """List all playlists from a channel
    Example: yt playlists --channel-id <your key>
    """

    playlists = get_channel_playlist(channel_id)
    for playlist in playlists:
        print(playlist.id, playlist.snippet.title)


if __name__ == "__main__":
    cli()
