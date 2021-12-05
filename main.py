from scrape.scraper import MoreleScraper
from scrape.alerts import DiscordAlert
from scrape.filter import LowerThanFilter
import os
from dotenv import load_dotenv
def main():
    load_dotenv()
    TOKEN = os.getenv("WEBHOOK_URL")
    Morele3080 = MoreleScraper(DiscordAlert(TOKEN), LowerThanFilter(13000))
    Morele3080.Run(60, 3090)  

if __name__ == "__main__":
    main()