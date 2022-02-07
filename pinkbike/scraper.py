"""Scrape pinkbike buy/sell."""

import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# from forex_python.converter import CurrencyRates

BASE_URL = "http://www.pinkbike.com/buysell/"
YEAR_PATTERN = re.compile("^2[0-9]{3}$")
# FOREX = CurrencyRates()


def scrape(item_id):
    """Scrape relevant information from pinkbike for the given item id."""
    url = BASE_URL + str(item_id)
    page = requests.get(url)
    if not page.ok:
        return None

    soup = BeautifulSoup(page.content, "html.parser")

    item = {"_id": item_id, "URL": url}
    title = soup.find("h1", class_="buysell-title").text.strip()
    year = title.split(" ", 1)[0]
    if YEAR_PATTERN.match(year):
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

    price = soup.find("div", class_="buysell-container buysell-price").text.strip()[1:]
    price, unit = price.split(" ")
    price = int(price.replace(",", ""))
    item["Price"] = price
    item["Price unit"] = unit
    # item["Price"] = FOREX.convert(unit, "USD", price, item["Last Repost Date"])

    item["Description"] = soup.find(
        "div", class_="buysell-container description"
    ).text.strip()

    seller_info = soup.find_all("span", class_="f11")[1].text.strip()
    seller_info = [s.strip() for s in seller_info.split("  ") if s.strip()]
    item["Location"] = seller_info[1]

    return item
