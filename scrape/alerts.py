
from abc import ABC, abstractmethod
from asyncio.windows_events import NULL
import json
import time
from typing import List

from requests.models import Response
from scrape.content.GPU_Base_Data import BaseGPU, ShopGPU
from requests import post
import json

from scrape.discord.Embed import DiscordEmbed
from scrape.discord.Webhook import DiscordWebhook, WebhookData

class BaseAlert(ABC):
    
    @abstractmethod
    def __init__(self, webhook_url: str) -> None:
        pass

    @abstractmethod
    def Format(self, gpu: BaseGPU):
        pass

    @abstractmethod
    def SendNotification(self, headers: dict = None):
        pass

class DiscordAlert(BaseAlert):

    webhook: WebhookData = None

    def __init__(self, webhook_url: str) -> None:
        self._webhook_url = webhook_url

    @property
    def webhook_url(self):
        return getattr(self, "_webhook_url", None)

    @webhook_url.setter
    def webhook_url(self, url: str):
        if isinstance(url, str):
            self._webhook_url = url

    def Format(self, gpus: List[ShopGPU]):
        webhook: WebhookData = DiscordWebhook()
        embeds = []
        for gpu in gpus:
            embed = DiscordEmbed()
            embed.title = f"{gpu.gpu_info.distributor}  {gpu.gpu_info.model}"
            embed.description = f"{gpu.gpu_info.price}"
            embed.url = f"https://{gpu.link}"
            embed.timestamp = gpu.timestamp
            embeds.append(embed)
        webhook.add_embeds(embeds)
        self.webhook = webhook

    def SendNotification(self, headers: dict = None):
        if headers is None:
            headers = {"Content-Type": "application/json"}

        if self.webhook is not None and self._webhook_url is not None:            
            response = post(self._webhook_url, data=json.dumps(self.webhook.to_dict()), headers=headers)
            
            print(response.content)
            
            
        


