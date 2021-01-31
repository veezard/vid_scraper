import requests
from bs4 import BeautifulSoup
from scrapers import Talk
from datetime import date
from dateutil.parser import parse as dateParser_
from scrapers import dateParse
from scrapers import removeParentheses
from scrapers import cleanSpeaker
from datetime import datetime


def scrape(start_date=date(1980, 1, 1)):

    year = datetime.today().year
    hostname = "http://www.birs.ca"
    talks = []
    while year < 3000:
        URL = "http://www.birs.ca/videos/" + str(year)
        try:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            workshop_divs = soup.find_all('div', class_="workshop-event")
            if len(workshop_divs) == 0:
                break
            for workshop_div in workshop_divs:
                try:
                    workshop = workshop_div.find(
                        'div', class_='event-title').text
                    video_divs = workshop_div.find_all('div', class_='video')
                    for video_div in video_divs:
                        try:
                            date = dateParse(
                                video_div.find(
                                    'span', {
                                        "itemprop": "datePublished"}).text)
                            if date < start_date:
                                year = 3000
                                break
                        except Exception as e:
                            raise e
                        a_tag = video_div.find(
                            'div', class_="actions").find('a')
                        if a_tag.text == "Watch video":
                            link = hostname + a_tag["href"]
                        else:
                            break
                        talk = Talk(link, workshop=workshop)
                        try:
                            speaker = video_div.find(
                                'div', class_="lecturer").find(
                                'span', {"itemprop": "author"}).text
                            talk.firstName, talk.lastName = cleanSpeaker(
                                speaker)
                        except BaseException:
                            pass
                        try:
                            talk.title = video_div.find(
                                'div', class_="talk-title").text
                        except BaseException:
                            pass
                        talks.append(talk)
                        print(talk)

                except BaseException:
                    pass
        except BaseException:
            pass
        year = year - 1

    return talks
