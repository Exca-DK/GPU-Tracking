from scrape.scraper import MoreleScraper
from scrape.alerts import DiscordAlert

def main():
    Morele3080 = MoreleScraper(DiscordAlert("WEBHOOK_TOKEN"))
    Morele3080.Run(60, 3090)  

if __name__ == "__main__":
    main()