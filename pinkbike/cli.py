"""CLI entrypoints through ``click`` bindings."""

import logging
from itertools import count
from pathlib import Path

import click
import pandas
from tqdm import tqdm

import pinkbike


@click.group()
@click.option(
    "--log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING"]),
    default="INFO",
    help="Set logging level for both console and file",
)
def cli(log_level):
    """CLI entrypoint."""
    logging.basicConfig(level=log_level)


@cli.command()
def version():
    """Print application version."""
    print(f"pinkbike version\t{pinkbike.__version__}")


@cli.command()
@click.option("--num_items", type=int)
@click.option("--output", type=click.Choice(["csv", "mongo"]))
@click.option("--start_id", type=int, default=2917101)
def scrape(num_items, output, start_id):
    """Scrape Pinkbike's buy/sell posts."""
    db = None
    if output == "mongo":
        db = pinkbike.db.connect()
        max_id = db.items.find_one(sort=[("_id", -1)])
        if max_id is not None:
            start_id = max_id["_id"] + 1

    items = []
    num_misses = 0
    for i in tqdm(count()):
        item = pinkbike.scraper.scrape(start_id + i)
        if item:
            num_misses = 0
            if db is not None:
                db.items.insert_one(item)
            else:
                items.append(item)
        else:
            num_misses += 1

        if num_items:
            if i >= num_items:
                break
        elif num_misses > 20:
            break

    if output == "csv":
        df = pandas.DataFrame(items)
        df.to_csv(Path(__file__).parents[1].resolve() / "items.csv", index=False)


@cli.command()
def delete_items():
    """Clear the db."""
    db = pinkbike.db.connect()
    db.items.delete_many({})
