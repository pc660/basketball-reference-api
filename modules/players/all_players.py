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
                        player_url = self.player_name[name]
                        player = player_url.split("/")[-1][:-5]
                        self.__access_data(player_url, player)
                 
        def __access_data(self, url, player):
                # data
                subject_list = {}
                subject_list["gamelog"] = ["pgl_basic"]
                subject_list["shooting"] = ["stats"]               
                subject_list["lineups"] = [
                        "lineups-5-man",
                        "lineups-4-man",
                        "lineups-3-man",
                        "lineups-2-man"
                ]
                subject_list["splits"] = ["stats"]
                subject_list["on-off"] = ["on-off"]
                for year in self.years:
                        for subject in subject_list:
                                url = url[:-5] + "/" + subject + "/" + str(year)
                                self.__access_player_subject_data(
                                    url, subject_list[subject], player)       
 
        def __access_player_subject_data(self, url, table_id, player):

                r = requests.get(url)
                dom = bs4.BeautifulSoup(r.text)
                player_data = {}
                player_data["index_name"] = player
                for name in table_id:
                        table = dom.find(id=name) 
                        table_name = []
                        if not table:
                                continue
                        for tag in table.find("thead").find_all("tr"):
                                if "over_header" in tag.attrs["class"]:
                                        continue
                                for t in tag.find_all("th"):
                                        table_name.append(t.attrs["data-stat"])
                                break                        
                        table_data = []
                        for tag in table.find("tbody").find_all("tr"):
                                i = 0
                                data = {}
                                for td in tag.find_all("td"):
                                        if len(td) == 0:
                                                i = i + 1
                                                continue      
                                        content = td.contents
                                        a_href = td.find_all("a")
                                        if a_href:
                                                content = ""
                                                for a in a_href:
                                                        content = content + \
                                                            a.contents[0] + "|"
                                                content = content[:-1]
                                        data[table_name[i]] = content
                                        i = i + 1
                                table_data.append(data)
                        player_data[name] = table_data
