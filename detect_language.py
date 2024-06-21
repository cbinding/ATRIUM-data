# see https://pypi.org/project/pycld2/
# and https://github.com/aboSamoor/pycld2
# pip install -U pycld2
import pycld2 as cld2
from urllib.parse import quote_plus # to urlencode a string value

# retrieve and parse resource metadata from a GoTriple page URL
import requests
import json
from bs4 import BeautifulSoup

# build URL for requested resource
# "https://www.gotriple.eu/documents/ftzenodo%3Aoai%3Azenodo.org%3A1434264"
#url = "https://doi.org/10.5281/zenodo.1434264"
BASE = "https://www.gotriple.eu/documents/"
id = "ftzenodo:oai:zenodo.org:1434264"
url = "{}{}".format(BASE, quote_plus(id))

# get the resource and parse out required details
response = requests.get(url, timeout=30)
soup = BeautifulSoup(response.text, features="html.parser")
tag = soup.find("script", id="__NEXT_DATA__")
if tag:
    # parse abstract text from the contents of this tag
    meta = json.loads(tag.contents[0])
    abstract = meta.get("props", {}).get("pageProps", {}).get("document", {}).get("abstract", [])[0].get("text", "")
    print(abstract)

    # detect language(s) of abstract
    isReliable, textBytesFound, details, vectors = cld2.detect(abstract, returnVectors=True)

    print(vectors)  
    # ((0, 288, 'ITALIAN', 'it'), (288, 630, 'ENGLISH', 'en'))  

    print(details)
    # (('ENGLISH', 'en', 69, 1150.0), ('ITALIAN', 'it', 30, 782.0), ('Unknown', 'un', 0, 0.0))
