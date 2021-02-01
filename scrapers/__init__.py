from datetime import date
from dateutil.parser import parse as dateParser_
import pickle
import re


class Talk:
    def __init__(
            self,
            link,
            title=None,
            firstName=None,
            lastName=None,
            abstract=None,
            workshop=None):
        self.link = link
        self.title = title
        self.firstName = firstName
        self.lastName = lastName
        self.abstract = abstract
        self.workshop = workshop

    def __str__(self):
        output = self.link
        if isinstance(self.firstName, str):
            output = output + "\n" + self.firstName + " "
            if isinstance(self.lastName, str):
                output = output + self.lastName
            output = output + ","
        if isinstance(self.title, str):
            output = output + "\n" + self.title
        if isinstance(self.abstract, str):
            output = output + "\n" + self.abstract
        if isinstance(self.workshop, str):
            output = output + "\n" + self.workshop
        output = output + "\n"
        return output

    def fullName(self):
        fullName = ""
        if self.firstName:
            fullName = fullName + self.firstName + " "
        if self.lastName:
            fullName = fullName + self.lastName
        return fullName.strip()


def dateParse(date):
    """ string -> date
    """
    return dateParser_(date).date()


def removeParentheses(text):
    return re.sub(r'\([^)]*\)', '', text)


def cleanSpeaker(speaker):
    speaker = removeParentheses(speaker)
    speaker = re.split(r',| and| AND| And|;|:', speaker)[0]
    words = [word.strip() for word in speaker.split(
        ' ') if word != '']
    word_num = len(words)
    if word_num == 0:
        return (None, None)
    elif word_num == 1:
        return (None, words[0].capitalize())
    else:
        return (" ".join(words[0:-1]), words[word_num - 1].capitalize())


def pickleLoader(pklFile):
    try:
        while True:
            yield pickle.load(pklFile)
    except EOFError:
        pass
