import os
import pytest

from src.crawler.crawler import Crawler
@pytest.mark.skip(reason="comment out if you have an internet connection")
def test_crawler():
    my_url = 'http://google.com'
    path_to_save = 'my_screenshot.png'
    html_content = Crawler().run(my_url, path_to_save)
    assert 'html' in html_content
    assert os.path.exists(path_to_save)
    os.remove(path_to_save)
