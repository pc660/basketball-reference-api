import os
import request
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
        try:
                r = request.get(url)
        except:
                return None
        return BeautifulSoup(r.text)

def all_players:
        def __init__(self, url):
                self.url = url

        def create_database(self):
                # iterate through a to z
                for i in range(ord("a", ord("z"))):
                        url = os.path.join(self.url, chr(i))
                        content = getSoupFromUrl(url)
