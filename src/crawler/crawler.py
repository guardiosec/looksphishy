import os
import conf
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(conf.LOGGER_NAME)

class Crawler:
    """
    This class contains all the methods related to URL crawling with enhanced error handling
    and Chrome configuration
    """
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "*",
        "Connection": "keep-alive",
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.42400.198 Safari/537.36")}

    def __init__(self, use_cache=False, max_retries=3, page_load_timeout=30):
        self.use_cache = use_cache
        self.max_retries = max_retries
        self.page_load_timeout = page_load_timeout
        self.driver = self.__init_driver()

    def run(self, url, path_to_save_screenshot, get_html=True):
        if self.use_cache and os.path.isfile(path_to_save_screenshot):
            logger.info(f"Screenshot already exists for {url}")
            if get_html:
                return self.get_html_content(url)
            return None

        retry_count = 0
        while retry_count < self.max_retries:
            try:
                # Set page load timeout
                self.driver.set_page_load_timeout(self.page_load_timeout)
                
                # Attempt to load the page
                self.driver.get(url)
                
                # Wait for page to be in ready state
                WebDriverWait(self.driver, self.page_load_timeout).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
                
                # Take screenshot
                self.save_screenshot(path_to_save_screenshot)
                
                if get_html:
                    return self.get_html_content(url)
                return None
                
            except (WebDriverException, TimeoutException) as e:
                retry_count += 1
                logger.warning(f"Attempt {retry_count} failed for {url}: {str(e)}")
                
                if retry_count >= self.max_retries:
                    logger.error(f"Max retries ({self.max_retries}) reached for {url}")
                    raise
                
                # Restart driver before retrying
                self.__restart_driver()
                time.sleep(2 * retry_count)  # Exponential backoff

    def save_screenshot(self, path_to_save):
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
            
            # Set window size before screenshot
            self.driver.set_window_size(1920, 1080)
            
            # Take screenshot
            self.driver.save_screenshot(path_to_save)
            logger.info(f"Screenshot saved to {path_to_save}")
        except Exception as e:
            logger.error(f"Failed to save screenshot: {str(e)}")
            raise

    def get_html_content(self, url):
        try:
            return self.driver.page_source
        except WebDriverException as e:
            logger.error(f"Failed to get HTML content: {str(e)}")
            raise

    def __init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--disable-gpu")  # Applicable to windows os only
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = Service(conf.CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def __restart_driver(self):
        """Cleanly close and restart the driver"""
        try:
            self.driver.quit()
        except Exception:
            pass
        self.driver = self.__init_driver()

    def __del__(self):
        """Ensure driver is closed when object is destroyed"""
        try:
            self.driver.quit()
        except Exception:
            pass