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
    print(f"Starting at: {start_id}")
    for i in tqdm(count()):
        item_id = i + start_id
        if item_id == 3023229:
            continue

        item = pinkbike.scraper.scrape(item_id)
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


@cli.command()
@click.option("--output", type=click.Choice(["csv", "mongo"]), default="csv")
def classify_fork_makes(output):
    """Classify fork make."""
    db = pinkbike.db.connect()
    fork_listings = db.items.find(
        {
            "Category": "Single Crown Forks",
            "Front Travel": {"$ne": "0 mm (Rigid)"},
            "Make": None,
            "$or": [
                {"Wheel Size": '27.5" / 650B'},
                {"Wheel Size": '29"'},
            ],
        }
    )
    fork_dicts = []
    for listing in fork_listings:
        if any(
            word in listing["Item"].lower()
            for word in ["wanted", "looking", "trade", "swap", "wtb"]
        ):
            continue
        make = None
        try:
            for fork in pinkbike.components.forks.values():
                for keyword in fork.keywords:
                    if keyword.lower() in listing["Item"].lower():
                        if make is not None:
                            raise Exception(
                                f"Multiple makes found for fork: {listing['_id']}"
                            )
                        make = fork.make
                        break
        except:  # noqa: E722
            if listing["_id"] == 2991267:
                continue
            elif listing["_id"] == 2955994:
                make = "Marzocchi"
            elif listing["_id"] == 3031629:
                make = "Giant"
            elif listing["_id"] == 3042625:
                make = "Fox"
            elif listing["_id"] == 3027934:
                make = "Marzocchi"
            else:
                raise
        if make and output == "mongo":
            db.items.update_one({"_id": listing["_id"]}, {"$set": {"Make": make}})
        elif output == "csv":
            fork_dicts.append(
                {
                    "ID": listing["_id"],
                    "Item": listing["Item"],
                    "Make": make,
                }
            )

    if output == "csv":
        df = pandas.DataFrame(fork_dicts)
        df.to_csv(Path(__file__).parents[1].resolve() / "forks.csv", index=False)


def _clean_string(string):
    chars = [",", "/", "mm"]
    for c in chars:
        string = string.replace(c, " ")
    string = string.replace("p 2", "p2")
    return string


def _search_keywords(listing, keywords):
    title = _clean_string(listing["Item"].lower()).split(" ")
    description = _clean_string(listing["Description"].lower()).split(" ")
    ret = None
    for k in keywords:
        if k.lower() in title:
            ret = k
            break
    if ret is None:
        for k in keywords:
            if k.lower() in description:
                ret = k
                break
    return ret


@cli.command()
@click.argument("make")
def classify_fork_models(make):
    """Parse fork model/damper/spring etc."""
    db = pinkbike.db.connect()
    listings = db.items.find(
        {
            "Make": make,
            # "$or": [
            #     {"Wheel Size": '27.5" / 650B'},
            #     {"Wheel Size": '29"'},
            # ],
        }
    )
    fork = pinkbike.components.forks[make]
    fork_model_dicts = []
    for listing in listings:
        model = _search_keywords(listing, fork.models)
        trim = _search_keywords(listing, fork.trims)
        spring = _search_keywords(listing, fork.springs)
        damper = _search_keywords(listing, fork.dampers)

        fork_model_dicts.append(
            {
                "ID": listing["_id"],
                "Year": listing["Year"] if "Year" in listing else None,
                "Name": listing["Item"],
                "Model": model,
                "Trim": trim,
                "Spring": spring,
                "Damper": damper,
            }
        )

    df = pandas.DataFrame(fork_model_dicts)
    df.to_csv(Path(__file__).parents[1].resolve() / "forks.csv", index=False)
