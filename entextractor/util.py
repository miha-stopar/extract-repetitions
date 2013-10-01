import requests
import time
import logging

logger = logging.getLogger("extractor")

def text_from_el(el):
    text = el.getText(" ")
    text = text.replace("&nbsp;", "  ") # two spaces to avoid regex expressions (\s?) in util being to greedy
    return text.strip()

def text_from_tags(tags):
    text = ""
    for tag in tags:
        text += tag.getText(" ")
    return text

def get_page_source(url):
    for _ in xrange(3): # try 3 times if some error occurs
        try:
            source = _get_page_source(url)
            return source
        except Exception:
            logger.error("Exception when downloading %s. After five seconds the download will be tried again." % url)
            time.sleep(5)
        
def _get_page_source(url):
    r = requests.get(url)
    if not r.ok:
        raise Exception 
    return r.text

