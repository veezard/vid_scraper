import pickle
import time
import requests
from bs4 import BeautifulSoup
from scrapers import Talk
from datetime import date, datetime
from dateutil.parser import parse as dateParser_
from scrapers import dateParse
from scrapers import removeParentheses
from scrapers import cleanSpeaker
from datetime import datetime
from selenium import webdriver
from scrapers import cleanSpeaker
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


def scrape(start_date=date(1980, 1, 1), outfile=None):
    talks = []
    hostname = "https://www.youtube.com"
    driver = webdriver.Firefox()
    delay = 10
    URL = "https://www.youtube.com/c/IhesFr/videos?view=0&sort=dd&flow=grid"

    try:
        driver.get(URL)
        time.sleep(60)  # during this minute, I manually scroll to the bottom
        # of the page

        contentsDiv = driver.find_elements_by_id('contents')[1]
        contentsHTML = contentsDiv.get_attribute('outerHTML')
        soup = BeautifulSoup(contentsHTML,
                             'html.parser')
        videoDivs = soup.find_all('ytd-grid-video-renderer')
        for videoDiv in videoDivs:
            infoDiv = videoDiv.find('a', id="video-title")
            link = hostname + infoDiv['href']
            youtubeTitle = infoDiv['title']
            label = infoDiv['aria-label']  # Can use label to determine date

            if speakerAndTitle := youtubeTitleToMaybeSpeakerAndTitle(
                    youtubeTitle):
                talk = Talk(link)
                talk.firstName, talk.lastName = cleanSpeaker(
                    speakerAndTitle
                    [0])
                talk.title = speakerAndTitle[1]
                talks.append(talk)
                print(talk)
                if outfile:
                    pickle.dump(talk, outfile)

    except BaseException:
        pass

    return talks


def youtubeTitleToMaybeSpeakerAndTitle(ytTitle):
    pieces = ytTitle.split(' - ')
    if len(pieces) == 1:
        return None
    name = pieces[0]
    title = pieces[1]
    if len(name.split(' ')) > 3:
        return None

    return (name, title)
