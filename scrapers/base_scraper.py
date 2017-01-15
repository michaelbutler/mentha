from scrapers import util
from scrapers.util import Settings, load_cookies, save_cookies


class BaseScraper:

    def __init__(self, vendor_name: str):
        self.driver = None
        self.vendor_name = vendor_name
        self.creds = Settings.get_creds()[vendor_name]
        self.settings = Settings.get_settings()[vendor_name]

    def iscrape(self):
        self.driver = util.get_driver()
        self.driver.get(self.settings["start_url"])

        # Inject cookies if available
        load_cookies(self.driver, self.vendor_name)

        result = self.scrape()

        # Store cookies to disk for next time
        save_cookies(self.driver, self.vendor_name)

        self.driver.quit()

        return result

    def scrape(self):
        """
        Subclasses should implement this.
        """
        raise RuntimeError("Scrapers must implement 'scrape' method")
