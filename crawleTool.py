import json
import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys


class SeriesData:
    title = ""
    description = ""
    episode = []

    def reprJSON(self):
        return dict(title=self.title,description=self.description,episode = self.episode)

    def to_json(self,indent=None):
        return json.dumps(self,default=lambda o:o.encode(),indent=indent)

class SeriesDatas:
    seriesDatas = []

    def reprJSON(self):
        return dict(seriesDatas=self.seriesDatas)


class EpisodeData:
    title = ""
    num = 0

    def reprJSON(self):
        return dict(title=self.title,num=self.num)
    def encode(self):
        return vars(self)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

class crawList:
    names=[]

    def __init__(self, j):
         self.__dict__ = json.loads(j)


class PythonOrgSearch:

    def __init__(self):
        file=open("./crawleList.json",mode='r')
        self.list =json.load(file)
        file.close()


    def search_in_python_org(self,url):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        option.add_argument('--incognito')
        option.add_experimental_option("detach", True)
        option.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=option)
        #self.driver.add_cookie({"name": "SESSDATA", "value": "fe6d0c15%2C1616126100%2C189c1*91",
                                #"domin": ".bilibili.com", "path": "/"
                                #})
        self.driver.get(url)
        time.sleep(5)
        try:
            button_login_close = self.driver.find_element_by_xpath(
                '//*[@id="close"]')
            button_login_close.click()
        except NoSuchElementException:
            print("can't find miniLogin close button")

        try:
            button_simple = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div[2]/ul/li[2]')
        except NoSuchElementException:
            print("can't find the element2")
        button_simple.click()
        try:
            button_login_close = self.driver.find_element_by_id("close")
            button_login_close.click()
        except NoSuchElementException:
            print("can't find miniLogin close button")

        Series = SeriesData()
        Series.title=self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[2]/div/div[2]/div[1]/span[1]').text

        Series.description=self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[2]/div/div[2]/div[4]/span').text

        #print(Series.title)
        #print(Series.description)

        mainPage_source = self.driver.page_source

        soup = BeautifulSoup(mainPage_source)
        episodes_box = soup.select("#app > div.media-tab-wrp > div.media-tab-content > div > div.media-tab-detail-l-wrp > div > div:nth-child(1) > div > div > div.sl-ep-list > ul")[0]
        #print(episodes_box)

        #i = 1
        for episodesBoxItem in episodes_box:
            if(episodesBoxItem.name!="li"):continue
            episode = EpisodeData()
            #print(type(episodesBoxItem))

            episode.title = episodesBoxItem['title']
            episode.num = int(episodesBoxItem.find('div',class_="misl-ep-index").get_text())
            #print(episode.num)
            #print(episode.title)
            Series.episode.append(episode)
            #i=i+1
        #print (json.dumps(Series.reprJSON(), cls=ComplexEncoder, ensure_ascii=False))
        #print (Series.reprJSON())
        #print(Series.__str__())
        #json.dumps(Series)
        self.driver.close()
        return Series
        #return json.dumps(Series.reprJSON(), cls=ComplexEncoder)


    def search_all(self):
        print(self.list)
        result=SeriesDatas()
        for url in self.list:
            result.seriesDatas.append(self.search_in_python_org(url))

        print(json.dumps(result.reprJSON(), cls=ComplexEncoder))
        file=open("./crawleResult.json",mode='w')
        file.write(''.join(json.dumps(result.reprJSON(), cls=ComplexEncoder)))
        file.close()

    def tearDown(self):
        self.driver.close()

search_tool =PythonOrgSearch()
search_tool.search_all()
