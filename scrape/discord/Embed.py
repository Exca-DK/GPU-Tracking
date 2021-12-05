from abc import ABC, abstractmethod
from json import dumps
from typing import Union
from datetime import datetime

from scrape.discord.EmbedExceptions import ColourOutOfRangeException, DatetimeException

class Embed(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def to_dict(self):
        pass

    

class DiscordEmbed(Embed):

    __slots__ = (
        '_title',
        '_url',
        '_type',
        '_description',
        '_timestamp',
        '_color',
        '_footer',
        '_image',
        '_thumbnail',
        '_video',
        '_provider',
        '_author',
        '_fields',
    )

    def __init__(self, **kwargs) -> None:
        self._title = kwargs.get("title")
        self._url = kwargs.get("url")
        self._type = kwargs.get("type", "rich")
        self._description = kwargs.get("description")
        self._timestamp = kwargs.get("timestamp")
        self._color = kwargs.get("color")
        if self._color:
            self._color(self._color)
        self._footer = kwargs.get("footer")
        self._image = kwargs.get("image")
        self._thumbnail = kwargs.get("thumbnail")
        self._video = kwargs.get("video")
        self._provider = kwargs.get("provider")
        self._author = kwargs.get("author")
        self._fields = kwargs.get("fields", [])

    @property
    def colour(self):
        return getattr(self, '_color', None)

    @colour.setter
    def colour(self, value: Union[int, str]):
        self._color = int(value, 16) if isinstance(value, str) else value
        if value not in range(16777216):
            raise ColourOutOfRangeException(value)

    @property
    def color(self):
        return self.colour

    @colour.setter
    def color(self, value: Union[int, str]):
        self.colour = value

    @property
    def title(self):
        return getattr(self, '_title', None)

    @title.setter
    def title(self, text: str):
        self._title = str(text) if not isinstance(text, str) else text

    @property
    def description(self):
        return getattr(self, '_title', None)

    @description.setter
    def description(self, text: str):
        self._description = str(text) if not isinstance(text, str) else text

    @property
    def url(self):
        return getattr(self, '_title', None)

    @url.setter
    def url(self, link: str):
        self._url = str(link) if not isinstance(link, str) else link

    @property
    def timestamp(self):
        return getattr(self, 'timestamp', None)

    @timestamp.setter
    def timestamp(self, value: datetime):
        if isinstance(value, datetime):
            self._timestamp = value
        else:
            raise DatetimeException(value)

    def to_dict(self):
        #fetch all slots atts
        result = {
            key[1:]: getattr(self, key)
            for key in self.__slots__
            if key[0] == '_' and hasattr(self, key)
        }

        #extra converts
        if result["timestamp"] is not None:
            result['timestamp'] = result['timestamp'].strftime("%Y-%m-%dT%H:%M:%S")

        return result


    def toJson(self):
        return dumps(self, default=lambda o: o.__dict__)

