import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as ec  # available since 2.26.0
import time

from scrapers import util
from scrapers.base_scraper import BaseScraper
from scrapers.util import Wait

ELEMENT_WAIT_TIMEOUT = 20


def parse_text_content(drv):
    x = 0
    inner_text = ""
    match_obj = None

    while x < 5:
        x += 1
        inner_text = Wait.wait_for(drv, '#loanDetails').text
        match_obj = re.search(r'Current Principal Balance \$ ([0-9,.]+)', inner_text, re.S | re.I)
        if match_obj is not None:
            break
        time.sleep(2)

    return {
        "balance": util.number_to_float(match_obj.group(1)),
        "full_text": inner_text,
    }


class Scraper(BaseScraper):

    def scrape(self):
        driver = self.driver

        # Enter email
        email_input = Wait.wait_for(driver, '#UserName')
        email_input.send_keys(self.creds["username"])
        email_input.send_keys(Keys.RETURN)

        time.sleep(3)

        try:
            # Assume we're logged in by checking the account info element
            logged_in = True
            Wait.wait_for(driver, ".logoutContainer .accountInfo")
        except TimeoutException:
            # If the element was not found, we're not logged in
            logged_in = False

        if logged_in:
            # Go to Load Details directly
            driver.get(self.settings["loan_details_url"])
        else:
            # Enter password
            password_input = Wait.wait_for(driver, "input#Password")
            password_input.send_keys(self.creds["password"])
            password_input.send_keys(Keys.RETURN)

            time.sleep(8)

            # Answer Security Question
            try:
                answer_input = Wait.wait_for(driver, "input#Answer")
                answer_input.send_keys(self.creds["secret_answer"])
                time.sleep(1)
                Wait.wait_click(driver, "input[name='RememberDevice'][value='Yes']")
                time.sleep(1)
                Wait.wait_click(driver, "form button.blueButton")
                time.sleep(1)
            except TimeoutException:
                # No security question needed
                pass

        WebDriverWait(driver, ELEMENT_WAIT_TIMEOUT).until(ec.title_contains("LoanDetails"))

        time.sleep(2)

        Wait.wait_for(driver, "#loanDetails #loanInformation")

        details = parse_text_content(driver)

        return details
