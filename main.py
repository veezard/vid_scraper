from datetime import date
from scrapers import mathtube
from scrapers import fields
from scrapers import ias
from scrapers import birs
from scrapers import pims
from scrapers import pirsa
from scrapers import simons
from scrapers import msri
from scrapers import Talk
from scrapers import dateParse
import pickle

# for talk in mathtube.scrape():
# print(talk)
outFile = open("talks_fields.p", "wb")
for talk in fields.scrape():
    pickle.dump(talk, outFile)

outFile.close()

# fields.scrape(start_date=date(2021, 1, 1))
