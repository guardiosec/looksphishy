import os
import conf
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(conf.LOGGER_NAME)


class Crawler:
    """
    This class contains all the methods related to URL crawling
    """
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "*",
        "Connection": "keep-alive",
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/86.0.42400.198 Safari/537.36")}

    def __init__(self, use_cache=False):
        self.driver = self.__init_driver()
        self.use_cache = use_cache

    def run(self, url, path_to_save_screenshot, get_html=True):
        if self.use_cache and os.path.isfile(path_to_save_screenshot):
            logger.info(f"Screenshot already exists for {url}")
        else:
            self.driver.get(url)
            self.save_screenshot(path_to_save_screenshot)

        if get_html:
            return self.get_html_content(url)

    def save_screenshot(self, path_to_save):
        self.driver.save_screenshot(path_to_save)
        logger.info(f"Screenshot saved to {path_to_save}")

    def get_html_content(self, url):
        self.driver.get(url)
        return self.driver.page_source

    @staticmethod
    def __init_driver():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        service = Service(conf.CHROME_DRIVER_PATH)
        return webdriver.Chrome(service=service, options=chrome_options)

    def __close_driver(self):
        self.driver.quit()
