from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

from scrapers.base_scraper import BaseScraper
from scrapers.util import Wait


class Scraper(BaseScraper):

    def scrape(self):
        driver = self.driver

        # Enter email
        email_input = Wait.wait_for(driver, '#userId-input-field')
        email_input.send_keys(self.creds["username"])

        # Enter password
        password_input = Wait.wait_for(driver, "#password-input-field")
        password_input.send_keys(self.creds["password"])

        time.sleep(1)

        password_input.send_keys(Keys.RETURN)

        time.sleep(4)

        # Detect if we need to do MFA
        try:
            mfa_button = Wait.wait_for(driver, "#logonDialog iframe#logonbox")
            mfa_button.click()
            print("Waiting 60 seconds, please perform the MFA and no other action")
            # TODO perform a wait loop here?
            time.sleep(100)
        except TimeoutException as ex:
            # We don't need MFA
            pass

        accounts = Wait.wait_for(driver, "#accountTiles")
        groups = accounts.find_elements_by_css_selector(".accounttilegroup")
        bank_accounts = groups[0].find_elements_by_css_selector(".account.segment")
        credit_cards = groups[1].find_elements_by_css_selector(".account.segment")

        account_summaries = []

        for el in bank_accounts:
            account_summaries.append(("bank", el.text))

        for el in credit_cards:
            if 'monthly FICO' in el.text:
                # skip the ad
                continue
            account_summaries.append(("credit", el.text))

        return account_summaries
