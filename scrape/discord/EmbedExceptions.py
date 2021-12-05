class ColourOutOfRangeException(Exception):
    def __init__(self, color: int) -> Exception:
        self.color = color

    def __str__(self) -> str:
        return repr(f"{self.color} is not a valid color. The proper color must be between 0 to 16777215 INT")

class DatetimeException(Exception):
    def __init__(self, datetime) -> Exception:
        self.datetime = datetime

    def __str__(self) -> str:
        return repr(f"{self.datetime} is not a valid datetime object. Expected datetime.datetime, received {self.datetime.__class__.__name__}")

class InvalidEmbedException(Exception):

    def __str__(self) -> str:
        return repr(f"Provided Embed must inherit from DiscordEmbed class")