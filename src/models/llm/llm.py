import logging
from functools import wraps
from bs4 import BeautifulSoup

import conf
from utils import timeit

logger = logging.getLogger(conf.LOGGER_NAME)

def handle_html_extraction_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Failed to extract html data. Error: {e}')
            return ''
    return wrapper

class HTMLTextExtractor:
    """
    Extracts specific text elements from HTML content.

    Methods
    -------
    extract_title():
        Extracts the title from HTML content.
    extract_meta_tags():
        Extracts specific meta tags from HTML content.
    run():
        Extracts title and meta tags, returning them as a dictionary.
    """

    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.llm_input = {}
    
    @handle_html_extraction_errors
    def extract_title(self):
        """Extracts the title from HTML content."""
        self.llm_input['title'] = self.soup.title.string if self.soup.title else ''
    
    @handle_html_extraction_errors
    def extract_meta_tags(self):
        """Extracts specific meta tags from HTML content."""
        target_meta_tags = {
            'title_og': {'attr_name': 'property', 'attr_value': 'og:title'},
            'title_tw': {'attr_name': 'name', 'attr_value': 'twitter:title'},
            'description': {'attr_name': 'name', 'attr_value': 'description'},
            'description_og': {'attr_name': 'property', 'attr_value': 'og:description'},
            'description_tw': {'attr_name': 'name', 'attr_value': 'twitter:description'}
            }

        for key, attrs in target_meta_tags.items():
            tag = self.soup.find('meta', attrs={attrs['attr_name']: attrs['attr_value']})
            self.llm_input[key] = tag['content'] if tag else ''

    def run(self):
        """
        Extracts title and meta tags, returning them as a dictionary.

        Returns
        -------
        dict
            Dictionary containing extracted title and meta tags.
        """
        self.extract_title()
        self.extract_meta_tags()
        return self.llm_input

class LLM(object):
    """
    Determines the industry of a website based on HTML content.

    """

    task = "What is the industry of this website based on the following data? Specify the industry only, and if it is impossible to determine, just put 'unknown'."

    @timeit
    def run(self, html_content):
        """
        Processes HTML content and returns the website's industry.

        Parameters
        ----------
        html_content : str
            The HTML content of the website.

        Returns
        -------
        str
            The industry of the website.
        """
        self.get_input_data(html_content)
        category = self.get_category()
        return category

    def get_input_data(self, html_content):
        """Extracts text data from HTML content."""
        self.input_data = HTMLTextExtractor(html_content).run()

    def get_category(self):
        """
        Abstract method to determine the industry.

        Returns
        -------
        str
            The industry of the website.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError
