import urllib3
import certifi
import bs4
import re

def get_ingredient_dicts():
    '''
    gets all products and ingredients_list for those products
    from the Jewel Osco website
    '''
    links=unique_links()
    return ingredients_list(links)

def get_links(link):
    '''
    Returns all links on a Jewel Osco page that map to product pages.

    Inputs:
    link(string): a link to a main page on Jewel Osco

    Outputs:
    absolute_list(list of strings): a list of absolute links to product pages.'''

    pm=urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    #bars= 'https://www.meijer.com/shop/en/snacks/granola-nutrition-bars/c/L3-262?icid=VW:Grocery:Snacks:Granola&NutritionBars'
    #bars= 'https://www.walmart.com/browse/food/new-year-new-you/976759_1567409_3170630_9741688'
    #bars= 'https://www.walmart.com/search/?query=protein%20bars&action=Create&rm=true'
    #bars= 'https://www.luckyvitamin.com/c-1390-nutrition-bars'
    #important_bars='https://www.jewelosco.com/shop/aisles/breakfast-cereal/breakfast-bars-bites.3441.html?sort=&page=1'
    html= pm.urlopen(url=link, method="GET").data
    link_list=[]
    absolute_list=[]
    soup=bs4.BeautifulSoup(html,'html5lib')
    for product in soup.find_all('a',class_='product-title'):
        link_list.append(product['href'])
    for relative in link_list:
        absolute_list.append('https://www.jewelosco.com' + relative)
    return absolute_list

def through_pages(link):
    '''
    Runs get_links on all pages of a given Jewel Osco main page

    Inputs:
    link(string): a link to start at

    Outputs:
    final_link_list(list of strings): a list of all product links on all pages of
    the link inputted
    '''
    num=int(link[-1])
    link=link[0:-1]
    final_link_list=[]
    doubles=[]
    links=[]
    for page in range(num,11):
        new_link=link+str(page)
        links.append(new_link)
    for new_link in links:
        final_link_list+=get_links(new_link)
    return final_link_list
                #final_link_list.append(i)
    #return final_link_list
def unique_links():
    '''
    Gets all unique links used in the project from Jewel Osco by using the
    get_links and through_pages functions on a variety of different starting
    pages.
    '''
    unique_list=[]
    starting_links= ['https://www.jewelosco.com/shop/aisles/breakfast-cereal/breakfast-bars-bites.3441.html?sort=&page=1'
    ,'https://www.jewelosco.com/shop/aisles/breakfast-cereal/breakfast-bars-bites.3441.html?sort=price&page=1'
    ,'https://www.jewelosco.com/shop/aisles/breakfast-cereal/breakfast-bars-bites.3441.html?sort=salesRank&page=1'
    ,'https://www.jewelosco.com/shop/aisles/breakfast-cereal/breakfast-bars-bites/granola-bars.3441.html?sort=salesRank&page=1'
    ,'https://www.jewelosco.com/shop/aisles/breakfast-cereal/breakfast-bars-bites/granola-bars.3441.html?sort=&page=1'
    ,'https://www.jewelosco.com/shop/aisles/breakfast-cereal/breakfast-bars-bites/cereal-bars-bites.3441.html?sort=&page=1'
    ,'https://www.jewelosco.com/shop/aisles/breakfast-cereal/breakfast-bars-bites/fruit-grain-bars.3441.html?sort=&page=1']
    for link in starting_links:
        uniques=set(through_pages(link))
        for i in uniques:
            if i not in unique_list:
                unique_list.append(i)
    return unique_list

def ingredients_list(link_list):
    '''
    Gets ingredients lists for each link in a list of links.

    Inputs:
    link_list(list of strings): A list of links to scrape ingredients lists from

    Outputs:
    ingredients_dict: A dictionary mapping products to their ingredients lists and
    the lengths of those aforementioned lists.
    '''
    ingredients_dict={}
    pm=urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    for link in link_list:
        html = pm.urlopen(url=link, method="GET").data
        soup = bs4.BeautifulSoup(html,'html5lib')
        title = soup.find('title').text
        title = re.search('.*?(?=-)',title)
        if soup!=None:
            ingredients_list=soup.find('div',class_="col-12 col-sm-12 col-md-6 col-lg-6 col-xl-6 flour body-m").text
            ingredients_list=ingredients_list.replace('\n','')
            ingredients_list=ingredients_list.strip()
            parentheses=re.findall('\(.*?(?=\))',ingredients_list)
            split_list=[]
            for group in parentheses:
                if len(group.split(','))>1:
                    splitted=group.split(',')
                    string_start=ingredients_list.find(group)
                    ingredients_list=ingredients_list.replace(group,'')
                    split_list.append((string_start,splitted))
            last=0
            new_list=[]
            for index,sublist in split_list:
                new_list+=ingredients_list[last:index].split(',')[:-1]
                new_list.append(sublist)
                last=index
            if new_list!=[]:
                new_list+=ingredients_list[last:].split(',')
            if new_list!=[]:
                ingredients_list=new_list
            if type(ingredients_list)==str:
                ingredients_list=ingredients_list.split(',')
            ingredients_list=[x for x in ingredients_list if x!='(' and x!=')']
            if len(ingredients_list)>1:
                ingredients_dict[title.group()]=[ingredients_list,len(ingredients_list)]
    return ingredients_dict
