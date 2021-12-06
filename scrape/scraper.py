from __future__ import annotations
from abc import ABC, abstractmethod
import time
from typing import Dict
from datetime import datetime
import random

from bs4 import BeautifulSoup
from requests import get

from scrape.filter import LowerThanFilter, HigherThanFilter, MinMaxFilter, BaseScraperFilter
from scrape.content.GPU_Base_Data import BaseGPU, ShopGPU
from scrape.alerts import BaseAlert



class BaseScraper(ABC):
    gpus: dict = None
    alert: BaseAlert = None
    filter: BaseScraperFilter = None
    user_agent: str = None

    @abstractmethod
    def __init__(self, alert: BaseAlert) -> None:
        pass

    @abstractmethod
    def GetData(self, model: str) -> BeautifulSoup:
        pass

    @abstractmethod
    def Parse(self, soup: BeautifulSoup):
        pass

    #TODO Check whether the offer is avaiable <MORELE TENDS TO UNAVAIABLE OFFERS>

    def Run(self, heartbeat: float, gpu_version: str):
        loop = True
        loops = 1
        print(f"heartbeat: {heartbeat}")
        print(f"gpu_version: {gpu_version}")

        while loop:
            data = self.GetData(gpu_version)
            gpus = self.Parse(data)
            self.Compare(gpus)
            print(loops)
            loops += 1           
            time.sleep(heartbeat+random.randrange(heartbeat/10))

    def Compare(self, data: Dict[int, ShopGPU]):
        counter = 0
        cache = []
        for key, value in data.items():
            if key not in self.gpus:
                self.gpus[key] = value
                cache.append(value)
                counter += 1
                if(len(cache)==9):
                    self.alert.Format(cache)
                    self.alert.SendNotification()
                    cache = []
                    counter = 0
                    return
        if(len(cache)>0):
            self.alert.Format(cache)
            self.alert.SendNotification()

        #remove gpu if it is no longer avaiable
        for key, value in self.gpus.items():
            if key not in data:
                self.gpus.pop(key)



class MoreleScraper(BaseScraper):

    def __init__(self, alert: BaseAlert, filter: BaseScraperFilter, headers: Dict[str, str]) -> BaseScraper:
        self.name = "Morele"
        self.website = "www.morele.net"
        self.url = "https://www.morele.net/kategoria/karty-graficzne-12/?q=rtx%20"
        self.gpus: dict = {}
        self.alert = alert
        self.filter = filter
            

    def GetData(self, model: str) -> BeautifulSoup:
            r = get(f"{self.url}{model}")
            return BeautifulSoup(r.content, "html.parser")            

    def Parse(self, soup: BeautifulSoup) -> dict[int, ShopGPU]:
        gpus = {}

        products = soup.find_all("div", class_="cat-product", recursive=True)
        for product in products:
            temp = product.find("a", class_="productLink")
            _price = product.find("div", class_="price-new").text.strip("\n").split(",")[0]
            _price = int(''.join(c for c in _price if c.isdigit()))
            gpu_info = BaseGPU(distributor=temp["title"].strip("Karta graficzna").split(" ", 1)[0],
                model=temp["title"].strip("Karta graficzna").split(" ", 1)[1], 
                price=_price)

            if self.filter.ShouldKeep(gpu_info):

                data = ShopGPU(gpu_info=gpu_info, 
                    link=self.website+temp["href"],
                    timestamp=datetime.utcnow(),
                    source=self.name
                    )

                gpus[int(product["data-product-id"])] = data

        return gpus


class XKomScraper(BaseScraper):

    def __init__(self, alert: BaseAlert, filter: BaseScraperFilter, headers: Dict[str, str]) -> BaseScraper:
        self.name = "Morele"
        self.website = "www.x-kom.pl"
        self.url = "https://www.x-kom.pl/szukaj?q=rtx%20GPUVERSION&f%5Bgroups%5D%5B5%5D=1&f%5Bcategories%5D%5B346%5D=1"
        self.gpus: dict = {}
        self.alert = alert
        self.filter = filter
        self.headers = headers
            

    def GetData(self, model: str) -> BeautifulSoup:
            self.url = self.url.replace("GPUVERSION", str(model))
            r = get(self.url, headers=self.headers)
            return BeautifulSoup(r.content, "html.parser")            

    def Parse(self, soup: BeautifulSoup) -> dict[int, ShopGPU]:
        gpus = {}
        products = soup.find_all("div", class_="sc-1yu46qn-4", recursive=True)
        for product in products:
            link = product.find("a", class_="sc-1h16fat-0")["href"]
            temp = product.find("h3")["title"]
            _price = product.find("span", class_="sc-6n68ef-3").text.strip("\n").split(",")[0]
            _price = int(''.join(c for c in _price if c.isdigit()))
       
            gpu_info = BaseGPU(distributor=temp.strip("Karta graficzna NVIDIA").split(" ", 1)[0],
                model=temp.strip("Karta graficzna NVIDIA").split(" ", 1)[1], 
                price=_price)

            if self.filter.ShouldKeep(gpu_info):
                data = ShopGPU(gpu_info=gpu_info, 
                    link=self.website+link,
                    timestamp=datetime.utcnow(),
                    source=self.name
                    )

                #x-kom doesn't provide us with an id so we create one manually
                gpus[hash(temp) % 10**8] = data

        return gpus


