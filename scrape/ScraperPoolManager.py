from concurrent.futures import ProcessPoolExecutor, as_completed
from scrape.scraper import BaseScraper

class ScrapeManager():
    def __init__(self, max_workers) -> None:
        self._running = False
        self.processes = []
        self._executor = ProcessPoolExecutor(max_workers=max_workers)

    @property
    def running(self):
        return self._running

    def AddScraper(self, scraper: BaseScraper, **kwargs):
        model = kwargs.get("model", None)
        heartbeat = kwargs.get("heartbeat", 60)
        if model is None:
            return
        self.processes.append(self._executor.submit(scraper.Run, heartbeat, model))

    def StopScrappers(self):
        if self._running:
            for thread in self._threads:
                thread.terminate()
            self._running = False
            #TODO use logging instead of printing in the future
            print("Canceled all scrapers")
