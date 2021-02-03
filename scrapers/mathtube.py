import requests
from bs4 import BeautifulSoup
from scrapers import Talk
from datetime import date
from dateutil.parser import parse as dateParser_
from scrapers import dateParse
from scrapers import removeParentheses
from scrapers import cleanSpeaker


def scrape(start_date=date(1980, 1, 1), process=None):  # process should be Talk -> None
    page_number = 0
    while page_number >= 0:
        URL = 'https://mathtube.org/videotype?page=' + str(page_number)
        page_number = page_number + 1
        try:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')

            talk_trs = []
            try:
                talk_trs = soup.find('tbody').find_all('tr')
            except BaseException:
                pass
            if len(talk_trs) == 0:
                page_number = -1  # This will break out of the outer loop if the current page has no talks
                break

            for talk_tr in talk_trs:
                date = dateParse(
                    talk_tr.find(
                        'td',
                        class_='views-field views-field-field-date').text)
                if (date < start_date):
                    page_number = -1  # This will break out of the outer loop if the current page has no talks
                    break
                link = "https://mathtube.org" + talk_tr.find(
                    'td', class_='views-field views-field-title').find('a')['href']
                if (talk := urlToTalk(link)):
                    if process:
                        process(talk)
                    print(talk)
        except BaseException:
            break

    return None


def urlToTalk(url):
    try:
        page = requests.get(url)
        talk = Talk(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            talk.title = soup.find('h1', class_='title gutter').text
        except BaseException:
            pass

        try:
            speaker = soup.find('span',
                                class_='views-field views-field-field-speaker').find('span',
                                                                                     class_='field-content').text
            talk.firstName, talk.lastName = cleanSpeaker(speaker)
        except BaseException:
            pass

        try:
            talk.workshop = "Mathtube- " + soup.find(
                'span', class_='views-field views-field-field-conference').find(
                'span', class_='field-content').text
        except BaseException:
            pass
        try:
            talk.abstract = soup.find(
                'div', class_='views-field views-field-field-abstract').find(
                'div', class_='field-content').text
        except BaseException:
            pass

        return(talk)

    except BaseException:
        return None
