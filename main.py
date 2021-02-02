from datetime import date
from scrapers import mathtube
from scrapers import fields
from scrapers import ias
from scrapers import birs
from scrapers import simons
from scrapers import ihes
from scrapers import msri
from scrapers import Talk
from scrapers import dateParse
import pickle
from scrapers import cleanSpeaker
from scrapers import pickleLoader


# for talk in simons.scrape(date(2021, 1, 1)):
# print(talk)

# ihes.scrape()

# outFile.close()

# fields.scrape(start_date=date(2021, 1, 1))
# infileName = "talks_fields_orig.p"
# outfileName = "talks_fields.p"
# outfile = open(outfileName, "wb")

# with open(infileName, "rb") as infile:
# for talk in pickleLoader(infile):
# if talk.workshop:
# talk.workshop = "Fields- " + talk.workshop.strip()
# pickle.dump(talk, outfile)
# print(talk)

# with open(infileName, "rb") as infile:
# for talk in pickleLoader(infile);
# talk.firstName, talk.lastName = cleanSpeaker(talk.fullName())
# pickle.dump(talk, outfile)
# print(talk.fullName())
# print(talk.firstName)
# print(talk.lastName)


# outfile.close()
