from __future__ import annotations
from abc import ABC, abstractmethod
import time
from typing import Dict
from datetime import datetime

from bs4 import BeautifulSoup
from requests import get

from scrape.content.GPU_Base_Data import BaseGPU, ShopGPU
from scrape.alerts import BaseAlert



class BaseScraper(ABC):
    @abstractmethod
    def __init__(self, alert: BaseAlert) -> None:
        pass

    @abstractmethod
    def GetData(self, model: str) -> BeautifulSoup:
        pass

    @abstractmethod
    def Parse(self, soup: BeautifulSoup):
        pass


class MoreleScraper(BaseScraper):

    def __init__(self, alert: BaseAlert) -> BaseScraper:
        self.name = "Morele"
        self.website = "www.morele.net"
        self.url = "https://www.morele.net/kategoria/karty-graficzne-12/?q=rtx%20"
        self.gpus: dict = {}
        self.alert = alert

    def Run(self, heartbeat: float, gpu_version: str):
        loop = True
        loops = 1
        while loop:
            data = self.GetData(gpu_version)
            gpus = self.Parse(data)
            self.Compare(gpus)
            print(loops)
            loops += 1
            time.sleep(heartbeat)
            

    def GetData(self, model: str) -> BeautifulSoup:
            r = get(f"{self.url}{model}")
            return BeautifulSoup(r.content, "html.parser")            

    def Parse(self, soup: BeautifulSoup) -> dict[int, ShopGPU]:
        gpus = {}

        products = soup.find_all("div", class_="cat-product", recursive=True)
        for product in products:
            
            temp = product.find("a", class_="productLink")
            gpu_info = BaseGPU(distributor=temp["title"].strip("Karta graficzna").split(" ", 1)[0],
                model=temp["title"].strip("Karta graficzna").split(" ", 1)[1], 
                price=product.find("div", class_="price-new").text.strip("\n").split(",")[0])

            data = ShopGPU(gpu_info=gpu_info, 
                link=self.website+temp["href"],
                timestamp=datetime.utcnow(),
                source=self.name
                )

            gpus[int(product["data-product-id"])] = data

        return gpus

    def Compare(self, data: Dict[int, ShopGPU]):
        counter = 0
        cache = []
        for key, value in data.items():
            if key not in self.gpus:
                self.gpus[key] = value
                cache.append(value)
                counter += 1
                if(len(cache)==9):
                    print("here2")
                    self.alert.Format(cache)
                    self.alert.SendNotification()
                    cache = []
                    counter = 0
                    return
        if(len(cache)>0):
            self.alert.Format(cache)
            self.alert.SendNotification()

