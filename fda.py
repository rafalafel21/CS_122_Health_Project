# Process FDA Additives webpage

import urllib3
import certifi
import bs4
import csv
import string
import re


COLORS = {'FD&C Blue #1', 'FD&C Blue #1 Lake', 'FD&C Blue #2', 
          'FD&C Blue #2 Lake', 'FD&C Green #3', 'FD&C Green #3 Lake',
          'FD&C Red #3', 'FD&C Red #3 Lake', 'FD&C Red #40', 
          'FD&C Red #40 Lake', 'FD&C Yellow #5', 'FD&C Yellow #5 Lake', 
          'FD&C Yellow #6', 'FD&C Yellow #6 Lake', 'Citrus Red #2'}

SUGAR_NAMES = {"Agave nectar", "Barbados sugar", "Barley malt", 
               "Barley malt syrup", "Beet sugar", "Brown sugar", 
               "Buttered syrup", "Cane juice", "Cane juice crystals", 
               "Cane sugar", "Caramel", "Carob syrup", "Castor sugar",
               "Coconut palm sugar", "Coconut sugar", "Confectioner's sugar",
               "Corn sweetener", "Corn syrup solids", "Date sugar", 
               "Dehydrated cane juice", "Demerara sugar", "Dextrin", 
               "Dextrose", "Evaporated cane juice", 
               "Free-flowing brown sugars", "Fructose", "Glucose", 
               "Glucose solids", "Golden sugar", "Golden syrup", 
               "Grape sugar", "High-Fructose Corn Syrup", "Honey", 
               "Icing sugar", "Invert sugar", "Malt syrup", "Maltodextrin", 
               "Maltol", "Mannose", "Maple syrup", "Molasses", "Muscovado", 
               "Palm sugar", "Panocha", "Powdered sugar", "Raw sugar", 
               "Refiner's syrup", "Rice syrup", "Saccharose", "Sorghum Syrup", 
               "Sugar", "Sweet Sorghum Syrup", "Treacle", "Turbinado sugar", 
               "Yellow sugar"}


def get_soup(fda_additives = "https://www.fda.gov/food/food-additives-petitions/food-additive-status-list"):
    '''
    Takes in url and returns soup object
    '''
    pm = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    html = pm.urlopen(url=fda_additives, method="GET").data

    soup = bs4.BeautifulSoup(html, "html5lib")

    return soup


def get_categories_dict(soup, id_name):
    '''
    Takes in soup object and id name for a category table and gets 
    categories from a table in the soup

    Returns: dict mapping category abbreviations to descriptions
    '''

    t = soup.find_all('div', class_="panel-collapse collapse in", 
                      id = id_name)
    rows = t[0].find_all('td')
    rows_txt = []

    for i in rows:
        txt = i.text
        rows_txt.append(txt)
    
    abbrevs = rows_txt[::2]
    desc = rows_txt[1::2]
    categories = dict(zip(abbrevs, desc))

    return categories


def full_categories_dict(soup):
    '''
    Combines two category dicts into one

    Returns: dict
    '''
    tech_effects = get_categories_dict(soup, id_name ="TechnicalEffects")
    status = get_categories_dict(soup, id_name ="RegulatoryStatus")

    all_categories = tech_effects.copy()
    all_categories.update(status)

    all_categories['COL'] = 'color additives'

    cat_with_id = {}
    init_id = 1

    for key, val in all_categories.items():
        cat_with_id[key] = [val, init_id]
        init_id += 1

    return cat_with_id


def write_to_csv(cat_with_id, csv_name = 'categories.csv'): 
    '''
    Take in categories dict and name for csv and writes to a csv
    '''
    with open(csv_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, val in d.items():
            writer.writerows([[key] + val])
    
    
def get_adds_to_ids_dict(soup):
    '''
    Takes in soup object and returns dict mapping additive 
    names to unique id numbers
    '''
    adds_to_ids = {}
    init_id = 1
    alphabet = list(string.ascii_uppercase)
    empties = []

    for i in alphabet:
        id_tag = 'ftn' + i
        sec = soup.find_all('h4', id=id_tag)
        adds = sec[0].next_sibling.next_sibling
        letter_lst = adds.find_all('li')
        

        for i in letter_lst:
            title = i.find('strong')
            if title != None:
                title_txt = title.text.lower()
                title_txt = title_txt.strip()
                title_txt = title_txt.strip('/"')
                adds_to_ids[title_txt] = init_id
                init_id += 1

    return adds_to_ids
  

def get_additives_dict(soup):
    '''
    Takes in soup object and returns dict mapping additive 
    names to categories
    '''
    additives = {}
    alphabet = list(string.ascii_uppercase)
    empties = []

    for i in alphabet:
        id_tag = 'ftn' + i
        sec = soup.find_all('h4', id=id_tag)
        adds = sec[0].next_sibling.next_sibling
        letter_lst = adds.find_all('li')
        

        for i in letter_lst:
            title = i.find('strong')
            if title != None:
                title_txt = title.text.lower()
                title_txt = title_txt.strip()
                title_txt = title_txt.strip('/"')
                labels = re.findall(r"[A-Z]{2,}\/?[A-Z]+", i.text)
                labels = set(labels)
                if labels == set():
                    empties.append(i.text)
                additives[title_txt] = labels
    
    for i in COLORS:
        i_lowered = i.lower()
        additives[i_lowered] = ['COL']

    for i in SUGAR_NAMES:
        i_lowered = i.lower()
        additives[i_lowered] = ['NUTRS']  

    additives['artificial ingredient'] = []

    sorted_dict = sorted(additives)     

    return additives


def additive_csvs(additives, adds_to_ids):
    '''
    Takes in additives dict and adds_to_ids dict and writes each to csv
    '''
    with open('adds_to_ids.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, val in adds_to_ids.items():
            writer.writerows([[key] + [val]])
     

    with open('additives.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, val in additives.items():
            for i in val:
                writer.writerows([[key] + [i]])


