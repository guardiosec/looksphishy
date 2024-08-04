import re
import urllib.parse
import os
import glob
import time
import logging
from functools import wraps

import conf

logger = logging.getLogger(conf.LOGGER_NAME)

def timeit(func):
    @wraps(func)
    def timed(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        instance = args[0] if args else None
        class_name = type(instance).__name__ if instance else ""
        logger.info(f"Function '{func.__name__}' of class '{class_name}' executed in {elapsed_time:.4f} seconds")
        return result
    return timed

def url_to_folder_name(url):
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    path = parsed_url.path
    folder_name = f"{hostname}{path}".replace("/", "_")
    folder_name = re.sub(r'[?&=]', '_', folder_name)
    folder_name = re.sub(r'[<>:"/\\|?*]', '_', folder_name)
    folder_name = folder_name.strip('_')

    return folder_name

def domain_to_url(domain):
    if domain.startswith(("http://", "https://")):
        return domain
    else:
        return f"http://{domain}"
def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def delete_all_embedding():

    json_files = glob.glob(os.path.join(conf.BRAND_FOLDER, '**', '*.json'), recursive=True)

    for json_file in json_files:
        try:
            os.remove(json_file)
            print(f"Deleted: {json_file}")
        except Exception as e:
            print(f"Error deleting {json_file}: {e}")

# Usage

if __name__ == '__main__':
    delete_all_embedding()