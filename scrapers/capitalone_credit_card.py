from selenium.webdriver.common.keys import Keys
import time

from scrapers.base_scraper import BaseScraper
from scrapers.util import Wait


class Scraper(BaseScraper):

    def scrape(self):
        driver = self.driver

        # Wait.wait_click_n(driver, ".container a.blue.external", 1)

        time.sleep(3)

        # Enter email
        email_input = Wait.wait_for(driver, '#username')
        email_input.send_keys(self.creds["username"])

        time.sleep(1)

        # Enter password
        password_input = Wait.wait_for(driver, "#password")
        password_input.send_keys(self.creds["password"])

        time.sleep(1)

        password_input.send_keys(Keys.RETURN)

        time.sleep(4)

        accounts = Wait.wait_for(driver, ".main section.left")
        credit_cards = accounts.find_elements_by_css_selector("article.bricklet")

        account_summaries = []

        for el in credit_cards:
            account_summaries.append(("credit", el.text))

        return account_summaries
