import textwrap

import click
import requests

from . import __version__


API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@click.command()
@click.version_option(version=__version__)
def main():
    """The hypermodern python project."""

    try:
        with requests.get(API_URL) as responses:
            responses.raise_for_status()
            data = responses.json()

        title = data["title"]
        extract = data["extract"]

        click.secho(title, fg="blue")
        click.echo(textwrap.fill(extract))
    except requests.exceptions.ConnectionError:
        click.secho("Sorry, Wikipedia API is unreacheble", fg="red")