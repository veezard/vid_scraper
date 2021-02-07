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


def scrape(start_date=date(1980, 1, 1), process=None):  # process should be Talk -> None

    year = datetime.today().year
    month = datetime.today().month
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    driver = webdriver.Firefox(firefox_options=fireFoxOptions)
    # driver = webdriver.Firefox()
    delay = 10
    while year < 3000:
        URL = "https://video-archive.fields.utoronto.ca/browse/" + \
            str(year) + "/" + str(month).zfill(2)

        try:
            driver.get(URL)
            time.sleep(4)

            watch_buttons = driver.find_elements_by_class_name(
                "talk-list-watch")
            if len(watch_buttons) == 0:
                year = 4000
                break
            for i in reversed(range(len(watch_buttons))):
                watch_buttons[i].click()
                time.sleep(3)
                talk = getTalk(driver)
                if process:
                    process(talk)
                print(talk)
                try:
                    date = driver.find_element_by_class_name(
                        "date-time").text[0:-2]
                    date = dateParse(date)
                    if date < start_date:
                        year = 3010
                        break
                except BaseException:
                    pass
                driver.back()
                time.sleep(1)
                watch_buttons = driver.find_elements_by_class_name(
                    "talk-list-watch")

        except BaseException:
            pass
        if month > 1:
            month = month - 1
        else:
            month = 12
            year = year - 1

    driver.quit()
    return None


def getTalk(driver):
    talk = Talk(driver.current_url)
    try:
        driver.find_element_by_class_name("navbar-burger").click()
        time.sleep(1)

    except BaseException:
        pass
    try:
        title = driver.find_element_by_class_name("talk-title").text
        talk.title = title
    except BaseException:
        pass
    try:
        speaker = driver.find_element_by_class_name("speaker").text
        talk.firstName, talk.lastName = cleanSpeaker(speaker)
    except BaseException:
        pass
    try:
        workshop = driver.find_element_by_class_name("event").text
        talk.workshop = "Fields- " + workshop

    except BaseException:
        pass
    return talk
