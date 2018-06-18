from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import defaultdict


def is_internal(path):
    if path != "":
        if path[0] == '/':
            return True
    else:
        False


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content,'html.parser')


def get_all_links(base_url, path, page_dict):
    soup = get_soup(base_url + path)
    print "current page = " + base_url + path
    for link in soup.find_all('a'):
        potential_path = link.get('href')
        print potential_path
        if potential_path is not None and is_internal(potential_path):
            if page_dict[potential_path] is False:
                continue
    page_dict[path] = True
    #print page_dict.items()
    return page_dict


#base_url = 'https://matchstickyvr.com'
#base_url = 'https://agroroasters.com'

root = '/'
roaster_filename = 'coffee_roasters_whitelist.txt'
f = pd.read_csv(roaster_filename, sep=",")
roasters = f['URL']

for roaster_url in roasters:
    print roaster_url
    pages = defaultdict(bool, {root: True})
    pages = get_all_links(roaster_url, root, pages)
    for path, visited in pages.items():
        if not visited:
            page_soup = get_soup(roaster_url)
            updated_pages = get_all_links(roaster_url, path, pages)
            updated_pages[path] = True
            #print (page_soup.prettify('utf-8'))
