from datetime import date, timedelta
from scrapers import mathtube
from scrapers import fields
from scrapers import ias
from scrapers import birs
from scrapers import simons
from scrapers import ihes
from scrapers import msri
from scrapers import Talk
from scrapers import dateParse
import pickle
from scrapers import cleanSpeaker
from scrapers import pickleLoader
from db import prepareSession
from db import addTalk
import argparse
import os


def main(start_date, dbFile):

    scriptDir = os.path.dirname(__file__)
    if start_date:
        start_date = dateParse(start_date)
    else:
        with open('{}/last_scan'.format(scriptDir), 'r') as dateFile:
            start_date = dateParse(dateFile.read())

    if dbFile:
        session = prepareSession(dbFile)
    else:
        session = prepareSession()

    scrapers = [
        birs.scrape,
        fields.scrape,
        ias.scrape,
        ihes.scrape,
        mathtube.scrape,
        msri.scrape,
        simons.scrape]

    for scraper in scrapers:
        scraper(
            start_date=start_date,
            process=(
                lambda talk: addTalk(
                    talk,
                    session)))

    with open('last_scan', 'w') as dateFile:
        dateFile.write(str(date.today() - timedelta(weeks=1)))

    os.remove('{}/geckdriver.log'.format(scriptDir))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--db',
        help='Database file. Defaults to videoarxiv.sqlite3')
    parser.add_argument(
        '--date',
        help='The date to start scraping from. If not specified, will use one week from previous scrape.')
    args = parser.parse_args()
    main(args.date, args.db)
