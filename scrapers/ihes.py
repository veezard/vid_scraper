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


def scrape(start_date=date(1980, 1, 1), process=None):  # process should be Talk -> None
    hostname = "https://www.youtube.com"
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    driver = webdriver.Firefox(firefox_options=fireFoxOptions)
    # driver = webdriver.Firefox()
    URL = "https://www.youtube.com/c/IhesFr/videos?view=0&sort=dd&flow=grid"

    try:
        driver.get(URL)
        # time.sleep(60)  # during this minute, I manually scroll to the bottom
        # of the page
        time.sleep(4)
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(2)
        html.send_keys(Keys.END)
        time.sleep(2)

        contentsDiv = driver.find_elements_by_id('contents')[1]
        contentsHTML = contentsDiv.get_attribute('outerHTML')
        soup = BeautifulSoup(contentsHTML,
                             'html.parser')
        videoDivs = soup.find_all('ytd-grid-video-renderer')
        for videoDiv in videoDivs:
            infoDiv = videoDiv.find('a', id="video-title")
            link = hostname + infoDiv['href']

            youtubeTitle = infoDiv['title']

            if speakerAndTitle := youtubeTitleToMaybeSpeakerAndTitle(
                    youtubeTitle):
                talk = Talk(link)
                date = urlToMaybeDate(link, driver)
                if date:
                    if date < start_date:
                        break
                talk.firstName, talk.lastName = cleanSpeaker(
                    speakerAndTitle
                    [0])
                talk.title = speakerAndTitle[1]
                print(talk)
                if process:
                    process(talk)

    except BaseException:
        pass

    return None


def youtubeTitleToMaybeSpeakerAndTitle(ytTitle):
    pieces = ytTitle.split(' - ')
    if len(pieces) == 1:
        return None
    name = pieces[0]
    title = pieces[1]
    if len(name.split(' ')) > 3:
        return None

    return (name, title)


def urlToMaybeDate(url, driver):
    try:
        driver.get(url)
        time.sleep(3)
        date = driver.find_element_by_id('date').text[1:]
        date = dateParse(date)
        return date
    except BaseException:
        return None
