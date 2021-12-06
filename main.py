import os
import ast
import time
from dotenv import load_dotenv

from scrape.scraper import MoreleScraper, XKomScraper
from scrape.alerts import DiscordAlert
from scrape.filter import LowerThanFilter
from scrape.ScraperPoolManager import ScrapeManager

def main():
    load_dotenv()
    TOKEN = os.getenv("WEBHOOK_URL")
    HEADERS = ast.literal_eval(os.getenv("HEADERS"))

    Morele3080 = MoreleScraper(DiscordAlert(TOKEN), LowerThanFilter(11000), HEADERS)
    xkom3060 = XKomScraper(DiscordAlert(TOKEN), LowerThanFilter(11000), HEADERS)
    Manager = ScrapeManager(3)
    Manager.AddScraper(Morele3080, heartbeat=60, model=3080)
    Manager.AddScraper(xkom3060, heartbeat=60, model=3060)

    time.sleep(300)

    Manager.StopScrappers()




if __name__ == "__main__":
    main()