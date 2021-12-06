import os
import ast
import time

from dotenv import load_dotenv

from scrape.scraper import MoreleScraper, XKomScraper, MediaexpertScraper, EuroScraper, ProlineScraper
from scrape.alerts import DiscordAlert
from scrape.filter import LowerThanFilter
from scrape.ScraperPoolManager import ScrapeManager

class App():

    def run(self):
        load_dotenv()
        TOKEN = os.getenv("WEBHOOK_URL")
        HEADERS = ast.literal_eval(os.getenv("HEADERS"))
        Morele3080 = MoreleScraper(DiscordAlert(TOKEN), LowerThanFilter(8000), HEADERS)
        XKom3080 = XKomScraper(DiscordAlert(TOKEN), LowerThanFilter(8000), HEADERS)
        Mediaexpert3080 = MediaexpertScraper(DiscordAlert(TOKEN), LowerThanFilter(8000), HEADERS)
        Euro3080 = EuroScraper(DiscordAlert(TOKEN), LowerThanFilter(8000), HEADERS)
        Proline3080 = ProlineScraper(DiscordAlert(TOKEN), LowerThanFilter(8000), HEADERS)

        Manager = ScrapeManager(5)
        Manager.AddScraper(Morele3080, heartbeat=60, model=3080)
        Manager.AddScraper(XKom3080, heartbeat=60, model=3060)
        Manager.AddScraper(Mediaexpert3080, heartbeat=60, model=3080)
        Manager.AddScraper(Euro3080, heartbeat=60, model=3060)
        Manager.AddScraper(Proline3080, heartbeat=60, model=3060)


    # time.sleep(300)

    # Manager.StopScrappers()



if __name__ == "__main__":
    app = App()
    app.run()