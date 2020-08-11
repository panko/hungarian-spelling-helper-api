#!/usr/bin/env python3

import requests
import json
from bs4 import BeautifulSoup

URL = "https://segits.be/j-ly/"

def has_no_attr(tag):
    print(tag)
    return not tag.attrs


def get_webpage_source(URL):
    # need to use session because there are too many redirects
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    return s.get(URL).text

def save_as_JSON(lista):
    out = {"j": [], "ly": []}
    for tag in lista:
        if "j" in tag.text:
            out["j"].append(tag.text)
        if "ly" in tag.text:
            out["ly"].append(tag.text)
    with open("words.json", "w", encoding='utf8') as outfile:
        json.dump(out, outfile, ensure_ascii=False)


def main():
    page_source = get_webpage_source(URL)
    soup = BeautifulSoup(page_source, 'html.parser')
    words = []
    for tag in soup.findAll('li'):
        if not tag.attrs:
            words.append(tag)
    save_as_JSON(words)

if __name__ == '__main__':
    main()
