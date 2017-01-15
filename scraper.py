#!/usr/bin/env python
import importlib
import sys

script_set = (
    "caliber_home_loans",
    "chase_bank",
    "capitalone_credit_card",
)

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        raise RuntimeError("Usage: python3 scraper.py <name of vendor>")

    scraper_type = sys.argv[1]

    if scraper_type not in script_set:
        raise RuntimeError(scraper_type + " not in available scraper list. Choices: " + ", ".join(script_set))

    module = importlib.import_module("scrapers." + scraper_type)

    try:
        scraper = module.Scraper(scraper_type)
        details = scraper.iscrape()
        print(details)
        print("\n")
    except Exception as ex:
        print("An exception occurred while trying to scrape: " + str(ex))
