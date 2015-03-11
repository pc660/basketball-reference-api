import os
import bs4
import requests
import thread
import pdb

class all_players:
        def __init__(self, baseurl, suburl):
                self.baseurl = baseurl
                self.suburl = self.baseurl + suburl
                self.player_name = {}
                # for testing purpose
                self.years = [2015]

        def create_database(self):
                # iterate through a to z
                # debug
                for i in range(ord("a"), ord("b")):
                        url = self.suburl + "/" + chr(i)
                        r = requests.get(url)
                        dom = bs4.BeautifulSoup(r.text)
                        self.get_player_url(dom, True)

        def get_player_url(self, Soup, current):
                if current:
                        for tag in Soup.body.findAll("strong"):
                                child = tag.children.next()
                                self.player_name[child.contents[0]] = \
                                        self.baseurl +  child.attrs["href"]

        def access_player_url(self):
                """Get player log from url"""
                for name in self.player_name:
                        self.__access_data(self.player_name[name])
                 
        def __access_data(self, url):
                # data
                subject_list = {}
                subject_list["gamelog"] = "pgl_basic"
                
                for year in self.years:
                        for subject in subject_list:
                                table_name = []
                                subject_data = []
                                url = url[:-5] + "/" + subject + "/" + str(year)
                                r = requests.get(url)
                                dom = bs4.BeautifulSoup(r.text)
                                table = dom.find(id=subject_list[subject]) 
                                if not table:
                                        continue
                                for tag in table.find("thead").find_all("th"):
                                        table_name.append(tag.attrs["data-stat"])
                                for tag in table.find("tbody").find_all("tr"):
                                        i = 0
                                        data = {}
                                        for td in tag.find_all("td"):
                                                if len(td) == 0:
                                                        i = i + 1
                                                        continue      
                                                content = ""
                                                if isinstance(td.children.next(),
                                                    bs4.element.Tag):
                                                        content = td.children.next().contents
                                                else:
                                                        content = td.contents
                                                data[table_name[i]] = content
                                                i = i + 1
