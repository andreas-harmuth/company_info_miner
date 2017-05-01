
import string
import random
import codecs
import json
import urllib.request
import requests
from bs4 import BeautifulSoup
import textract
import PyPDF2



def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for x in range(size))




def format_reader(input):
    reader = codecs.getreader("utf-8")
    return reader(input)



def download_file(download_url):
    response = requests.get(download_url)
    name = 'annual_report.pdf'
    with open(name , 'wb') as f:
        f.write(response.content)

    return name



def cvr_all_info(cvr,country = 'dk'):
    # Load the request with the random header
    req = urllib.request.Request(url='http://cvrapi.dk/api?search=' + str(cvr)
                                 + '&country=' + country,
                                 headers={'User-Agent': random_generator()})

    # Open and encode the response
    with urllib.request.urlopen(req) as response:

        reader = codecs.getreader("utf-8")
        return json.load(reader(response))




def proofdk_annual_report(cvr):
    # Load the request with the random header
    res = urllib.request.urlopen('https://datacvr.virk.dk/data/visenhed?enhedstype=virksomhed&id=' + str(cvr))
    reader = codecs.getreader("utf-8")
    soup = BeautifulSoup(reader(res).read(),"lxml")

    div = soup.findAll("div", {"class": "regnskabs-download"})
    loc = download_file(div[0].findAll('a', href=True)[0]['href'])

    pdfFileObj = open(loc, 'rb')  # 'rb' for read binary mode

    # TODO: read the pdf





proofdk_annual_report(32163289)