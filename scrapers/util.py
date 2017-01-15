import configparser
import os
import time

import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

ELEMENT_WAIT_TIMEOUT = 15
CLICK_TIMEOUT = 5


class Wait:
    @staticmethod
    def wait_click(drv, css_selector):
        WebDriverWait(drv, ELEMENT_WAIT_TIMEOUT).until(ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        element = drv.find_element_by_css_selector(css_selector)
        element.click()
        time.sleep(CLICK_TIMEOUT)

    @staticmethod
    def wait_click_n(drv, css_selector, n):
        """
        Click the nth element that matches the css_selector. Raises exception if element cannot be found
        """
        WebDriverWait(drv, ELEMENT_WAIT_TIMEOUT).until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        elements = drv.find_elements_by_css_selector(css_selector)
        if not elements or 1 <= n < len(elements):
            elements[n - 1].click()
            time.sleep(CLICK_TIMEOUT)
        else:
            raise Exception("Cannot click element " + str(n) + " of css selector " + css_selector)

    @staticmethod
    def wait_for(drv, css_selector) -> WebElement:
        WebDriverWait(drv, ELEMENT_WAIT_TIMEOUT).until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        return drv.find_element_by_css_selector(css_selector)


def number_to_float(num):
    num = str(num)
    num = num.replace(",", "")
    num = float(num)
    return num


class Settings:
    settings = configparser.ConfigParser()
    creds = configparser.ConfigParser()

    @staticmethod
    def get_settings() -> configparser.ConfigParser:
        if not Settings.settings.sections():
            Settings.settings = configparser.ConfigParser()
            Settings.settings.read('settings.ini')
        return Settings.settings

    @staticmethod
    def get_creds() -> configparser.ConfigParser:
        if not Settings.creds.sections():
            Settings.creds = configparser.ConfigParser()
            Settings.creds.read('credentials.ini')
        return Settings.creds


def get_driver() -> WebDriver:
    """
    Returns a WebDriver implementation, in this case Firefox
    """
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", Settings.get_settings()["general"]["desktop_user_agent"])
    binary = FirefoxBinary(Settings.get_settings().get("general", "firefox_binary"))

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)

    return driver


def load_cookies(driver, vendor_name):
    # Insert cookies if available
    if os.path.isfile(vendor_name + ".cki"):
        cookies = pickle.load(open(vendor_name + ".cki", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)


def save_cookies(driver: WebDriver, vendor_name: str):
    pickle.dump(driver.get_cookies(), open(vendor_name + ".cki", "wb"))
