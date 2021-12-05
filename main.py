from scrape.scraper import MoreleScraper
from scrape.alerts import DiscordAlert
import os
from dotenv import load_dotenv
def main():
    load_dotenv()
    TOKEN = os.getenv("WEBHOOK_URL")
    Morele3080 = MoreleScraper(DiscordAlert(TOKEN))
    Morele3080.Run(60, 3090)  

if __name__ == "__main__":
    main()