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


def scrape(start_date=date(2005, 1, 1), outfile=None):
    talks = []
    hostname = "https://www.msri.org"
    URL = "https://www.msri.org/events/semester?from=2021-01-01&to=2021-05-31"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    rightPanel = soup.find('ul', id="semester-menu")
    years = rightPanel.find_all('li', recursive=False)
    semesterLinks = [hostname + a['href']
                     for year in years for a in year.find_all('a')]
    for semesterLink in semesterLinks:

        page = requests.get(semesterLink)
        soup = BeautifulSoup(page.content, 'html.parser')
        workshopLis = soup.find('div',
                                class_="page-content").find('ol',
                                                            recursive=False).find_all('li',
                                                                                      recursive=False)

        for workshopLi in workshopLis:
            date = dateParse(
                cutStringUntilSequence(
                    workshopLi.find('time').text,
                    ["(", "-"]))
            print(date)
            if date < start_date:
                break
            workshop = "MSRI- " + workshopLi.find('a').text
            talkLis = workshopLi.find(
                'ul', class_="schedules-with-videos").find_all('li', recursibe=False)
            if len(talkLis) < 4:
                workshop = None
            for talkLi in talkLis:
                try:
                    link = hostname + talkLi.find('a',
                                                  recursive=False)['href']
                    title = talkLi.find('a', recursive=False).text
                    talk = Talk(link, title=title)
                    talk.workshop = workshop
                    if (abstract := urlToMaybeAbstract(link)):
                        talk.abstract = abstract

                    try:
                        speaker = talkLi.find(
                            'span', class_="person").text.strip()
                        talk.firstName, talk.lastName = cleanSpeaker(speaker)
                    except BaseException:
                        pass
                    if talk.firstName is None and talk.lastName is None:
                        break
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
                    abstract, ["No Abstract Uploaded", "No Notes/Supplements Uploaded"]).strip()
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
