# this is an exact copy of Desktop.scrape_meijer.py

import urllib3
import certifi
import bs4
import re


def crawl_store():
    '''
    Crawls the directeat store website and collects 
    the ingredients of all health bars

    Outputs: dictionary mapping product to ingredient list
    and ingredient list length
    '''
    final_links = []
    ingredients = {}
    beg_half = "http://directeats.com/food/snacks/bars?page="
    end_half = "&sort=Realware.Plugin.ProductSort.PriceLowHigh"
    for i in range(1, 14):
        new_page = beg_half + str(i) + end_half
        final_links += crawl_page(new_page)
    
    for link in final_links:
        link_ing = scrape_page(link[1])
        ingredients[link[0]] = [link_ing, len(link_ing)]
    
    return ingredients

def crawl_page(url):
    '''
    Takes in a url and finds all other links
    on the page 

    Input: url (str): to crawl
    Output: List of links to scrape
    '''
    pm = urllib3.PoolManager(
        cert_reqs = "CERT_REQUIRED",
        ca_certs = certifi.where()
        )

    link_list = []
    bars = url
    html = pm.urlopen(url=bars, method="GET").data

    soup = bs4.BeautifulSoup(html, "html5lib")
    
    for link in soup.find_all('a'):
        rel_link = link.get('href')
        if "/product" in rel_link:
            name = " ".join(rel_link.split("/")[2].split("-"))
            if (name, rel_link) not in link_list:
                link_list.append((name, rel_link))

    for i, link in enumerate(link_list):
        link_list[i] = (link[0], "http://directeats.com" + link[1])
        
    return link_list

def scrape_page(url):
    '''
    Scrapes page for ingredient list. If there are sublists
    of ingredients, it will provide a nested list within
    the main list of ingredients.

    Input: 
        url (str): url of health bar to scrape
    
    Output:
        list of ingredients for a given health bar
    '''
    pm = urllib3.PoolManager(
        cert_reqs = "CERT_REQUIRED",
        ca_certs = certifi.where()
        )

    bars = url
    html = pm.urlopen(url=bars, method="GET").data

    soup = bs4.BeautifulSoup(html, features = "html.parser")
    ingredients = soup.find("div", class_ = ["container-fluid"])
    ingredient_script = str(ingredients.find("script")).split("var str = ")[1].split(";")
    if ingredient_script[0] != '""':
        ingredient_script[0] = ingredient_script[0].replace("*", "")
        ingredient_script[0] = ingredient_script[0].replace("†", "")
        ingredient_script[0] = ingredient_script[0].replace('"', "")
        ingredient_script[0] = ingredient_script[0].replace('.', "")
        sublist = re.findall('\(([^)]+)', ingredient_script[0])
        split_list=[]
        for group in sublist:
            split_list.append(group.split(','))
        split = ingredient_script[0].split(",")
        for x, i in enumerate(split): 
            for j in split_list: 
                if '(' in i and ')' not in i: 
                    s= '' 
                    for k in range(len(i)): 
                        if k > i.index('('): 
                            s+=i[k] 
                        if s in j: 
                            split[x] = j
                elif ')' in i and '(' not in i: 
                    s='' 
                    for k in range(len(i)): 
                        if k < i.index(')'): 
                            s+=i[k] 
                        if s in j:
                            if i in split: 
                                split.remove(i) 
                elif ')' in i and '(' in i: 
                    s= '' 
                    for k in range(len(i)): 
                        if k > i.index("(") and k < i.index(')'): 
                            s+=i[k] 
                        if s in j: 
                            split[x] = j
                else: 
                    if i in j:
                        if i in split: 
                            split.remove(i)    
        ingredient_list = split              
    else:
        ingredient_list = "Empty"

    return ingredient_list

