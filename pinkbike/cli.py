"""CLI entrypoints through ``click`` bindings."""

import logging
import re
from datetime import datetime
from itertools import count
from pathlib import Path

import click
import pandas
import requests
from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates
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
def scrape():
    """Scrape Pinkbike's buy/sell posts."""
    start_id = 2917101
    base_url = "http://www.pinkbike.com/buysell/"
    c = CurrencyRates()
    year_pattern = re.compile("^2[0-9]{3}$")
    items = []
    for i in tqdm(count()):
        item_id = start_id + i
        url = base_url + str(item_id)
        page = requests.get(url)
        if not page.ok:
            continue
        soup = BeautifulSoup(page.content, "html.parser")

        item = {"ID": item_id}
        title = soup.find("h1", class_="buysell-title").text.strip()
        year = title.split(" ", 1)[0]
        if year_pattern.match(year):
            item["Year"] = year
            title = title.split(" ", 1)[1]
        item["Item"] = title

        details = soup.find_all("div", class_="buysell-details-column")
        for d in details:
            detail_lines = []
            for line in d.text.splitlines():
                detail_lines.append(line.strip().split(":"))

            j = 0
            while j < len(detail_lines):
                detail_line = detail_lines[j]
                key = detail_line[0]
                if key:
                    if key == "Still For Sale":
                        j += 1
                        item[key] = detail_lines[j] == "Sold"
                    elif key == "Condition":
                        extras = [
                            s.strip()
                            for k in range(1, len(detail_line))
                            for s in detail_line[k].split("  ")
                            if s
                        ]
                        item[key] = extras[0]
                        for k in range(1, len(extras), 2):
                            item[extras[k]] = extras[k + 1]
                    else:
                        item[key] = detail_line[1].strip()
                        if "Date" in key:
                            item[key] = datetime.strptime(
                                item[key].split(" ")[0], "%b-%d-%Y"
                            )
                        elif "Count" in key:
                            item[key] = int(item[key].replace(",", ""))
                j += 1

        price = soup.find("div", class_="buysell-container buysell-price").text.strip()[
            1:
        ]
        price, unit = price.split(" ")
        price = int(price.replace(",", ""))
        item["Price"] = c.convert(unit, "USD", price, item["Last Repost Date"])

        items.append(item)

        if i > 1000:
            break

    df = pandas.DataFrame(items)
    df.to_csv(Path(__file__).parents[1].resolve() / "items.csv", index=False)
