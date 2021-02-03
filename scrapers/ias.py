from scrapers.simons import urlToMaybeAbstract
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


def scrape(start_date=date(1980, 1, 1), process=None):  # process should be Talk -> None
    hostname = "https://www.ias.edu"
    page_number = 1
    while page_number >= 0:
        URL = 'https://www.ias.edu/video?tags=All&page=' + str(page_number)
        page_number = page_number + 1
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            talkDivs = soup.find(
                'div', class_="views-infinite-scroll-content-wrapper clearfix").find_all(
                'div', recursive=False)
            for talkDiv in talkDivs:
                try:
                    date = talkDiv.find(
                        'div',
                        class_="field field--name-field-date-single field--type-datetime field--label-hidden").text
                    date = dateParse(date)
                    if date < start_date:
                        page_number = -1
                        break
                    title = talkDiv.find(
                        'h3', class_="teaser-full-width__label").text.strip()
                    link = hostname + talkDiv.find(
                        'h3', class_="teaser-full-width__label").find('a')['href']
                    talk = Talk(link, title=title)

                    if (abstract := urlToMaybeAbstract(link)):
                        talk.abstract = abstract

                    try:
                        speaker = talkDiv.find(
                            'div', class_="teaser-full-width__detail").text.strip()
                        talk.firstName, talk.lastName = cleanSpeaker(speaker)
                    except BaseException:
                        pass

                    if process:
                        process(talk)
                    print(talk)

                except BaseException:
                    pass

        except BaseException:
            break

    return None


def urlToMaybeAbstract(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        abstract = soup.find(
            'div',
            class_='field field--name-body field--type-text-with-summary field--label-hidden').text.strip()

        return abstract

    except BaseException:
        return None
