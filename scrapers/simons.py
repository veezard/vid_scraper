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
        URL = 'http://scgp.stonybrook.edu/video_portal/index.php?page=' + str(
            page_number)
        page_number = page_number + 1

        try:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            new_talks_div = soup.find('div', class_="col-lg-7 col-md-9")
            talk_divs = new_talks_div.find_all('div', class_="col-xs-8")

            if len(talk_divs) == 0:
                page_number = -1
                break

            for talk_div in talk_divs:
                link = hostname + talk_div.find('a',
                                                class_="btn btn-primary btn-xs")['href']
                talk = Talk(link)
                dataField = talk_div.text
                # Tokens are used in the regular expression to extract talk
                # data
                all_tokens = "(\nTitle: |\nEvent: |\nName: |\nDate: |\nLocation: |\nview video)"
                tokens = {
                    'title': '\nTitle: ',
                    'workshop': '\nEvent: ',
                    'speaker': '\nName: ',
                    'date': '\nDate: '}

                try:
                    date = dateParse(
                        re.search(
                            '%s(.*?)%s' %
                            (tokens['date'],
                             all_tokens),
                            dataField,
                            flags=re.DOTALL | re.MULTILINE).group(1).replace(
                            '@',
                            ''))
                    if date < start_date:
                        page_number = -1
                        break
                except BaseException:
                    pass

                try:
                    speaker = re.search(
                        '%s(.*?)%s' %
                        (tokens['speaker'],
                         all_tokens),
                        dataField,
                        flags=re.DOTALL | re.MULTILINE).group(1).strip()
                    talk.firstName, talk.lastName = cleanSpeaker(speaker)
                except BaseException:
                    pass

                try:
                    title = re.search(
                        '%s(.*?)%s' %
                        (tokens['title'],
                         all_tokens),
                        dataField,
                        flags=re.DOTALL | re.MULTILINE).group(1).strip()
                    if title != '':
                        talk.title = title
                except BaseException:
                    pass

                try:
                    workshop = re.search(
                        '%s(.*?)%s' %
                        (tokens['workshop'],
                         all_tokens),
                        dataField,
                        flags=re.DOTALL | re.MULTILINE).group(1).strip()
                    if workshop != '':
                        talk.workshop = "Simons- " + workshop
                except BaseException:
                    pass

                if (abstract := urlToMaybeAbstract(link)):
                    talk.abstract = abstract

                talks.append(talk)
                print(talk)
                if outfile:
                    pickle.dump(talk, outfile)

        except BaseException:
            pass
    return talks


def urlToMaybeAbstract(url):
    try:
        page = requests.get(url)
        talk = Talk(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        dataField = soup.find_all('div', class_='col-md-12')[2].text

        abstract = re.search(r'\nAbstract: (.*)', dataField).group(1).strip()
        if abstract != '':
            return abstract
        else:
            return None
    except BaseException:
        return None
