import requests
import re
from bs4 import BeautifulSoup
from scrapers import Talk
from datetime import date
from dateutil.parser import parse as dateParser_
from scrapers import dateParse
from scrapers import removeParentheses
from scrapers import cleanSpeaker
import pickle


def scrape(start_date=date(1980, 1, 1), outfile=None):
    talks = []
    page_number = 1
    hostname = "http://scgp.stonybrook.edu"
    while page_number >= 0:
        pass

    return talks


def urlToMaybeAbstract(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        sections = soup.find_all('section')
        sections = map(lambda x: x.text, sections)
        # return list(sections)[2]
        for section in sections:
            regSearch = re.search(
                r'\nAbstract(.*?)\n(.*)',
                section,
                flags=re.DOTALL | re.MULTILINE)
            try:
                abstract = regSearch.group(2).strip()
                abstract = cutStringUntilSequence(
                    abstract, ["No Abstract Uploaded"]).strip()
                if abstract != '':
                    return abstract

            except BaseException:
                pass

    except BaseException:
        return None


def cutStringUntilSequence(string, sequences):
    for sequence in sequences:
        try:
            string = string[0:string.index(
                sequence)]
        except BaseException:
            pass
    return string
