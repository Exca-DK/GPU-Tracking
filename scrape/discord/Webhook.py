from abc import ABC, abstractmethod
from typing import List, Union
from scrape.discord.Embed import DiscordEmbed
from scrape.discord.WebhookException import EmbedsAmountExcedeed

class WebhookData(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def to_dict(self):
        pass

class DiscordWebhook():
    __slots__ = ("_content",
        "_embeds"
    )
    def __init__(self, **kwargs) -> None:
        self._content: str = kwargs.get("content", "")
        self._embeds: list = kwargs.get("embeds", [])

    @property
    def embeds(self):
        return getattr(self, '_embeds', None)
    
    def add_embeds(self, embeds: Union[DiscordEmbed, List[DiscordEmbed]]):
        if isinstance(embeds, list):
            for embed in embeds:
                if len(self._embeds) < 9:
                    self._embeds.append(embed)
                else:
                    raise EmbedsAmountExcedeed()
        else:
            if len(self._embeds) < 9:
                self._embeds.append(embeds)

    def to_dict(self):
        result = {
            key[1:]: getattr(self, key)
            for key in self.__slots__
            if key[0] == '_' and hasattr(self, key)
        }

        if result["embeds"] is not None:
            result["embeds"] = [embed.to_dict() for embed in result["embeds"] 
                if isinstance(embed, DiscordEmbed)]

        return result
