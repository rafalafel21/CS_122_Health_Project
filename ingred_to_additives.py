# Match ingredient names to FDA Additive names

import fda
import re
import jellyfish
import csv
import jewel_plus_direct as merge

def classify_ingred_lists():
    '''
    Create dict mapping product names to lists of additives in the product
    '''
    ingred_dict = merge.merge_them()

    products_to_additives = {} # map products to additives 
                               # (where additive names reflect the FDA name,
                               # not the name in the product's ingred list)  
    soup = fda.get_soup()
    additives = fda.get_additives_dict(soup)

    for product, val in ingred_dict.items():
        products_to_additives[product] = []
        ingred_list = val[0]

        for i in ingred_list:
            if type(i) == str:
                matched_add = ingred_in_additive(additives, i)
                orig_ing_name = i

            else:
                for j in i:

                    matched_add = ingred_in_additive(additives, j)
                    orig_ing_name = j
            
            if matched_add != None:
                products_to_additives[product].append((matched_add, orig_ing_name))
    
    return products_to_additives


def csv_products_to_additives(products_to_additives):
    '''
    Write products_to_additives dict to csv
    '''
    with open('products_to_additives.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, val in products_to_additives.items():
            for i in val:
                print(key, i)
                writer.writerows([[key] + [i[0]] + [i[1]]])




def ingred_in_additive(additives, ingred_name):
    '''
    Check if an ingredient is an additive and return name of additive
    if it is, and None if it isn't

    Inputs:
        additives: dict of all additives
        ingred_name: str

    Returns: str or None
    '''

    ingred = ingred_name.lower()

    if 'artificial' in ingred:
        return 'artificial ingredient'
    
    else:
        for key in additives:
            jw_score = jellyfish.jaro_winkler(key, ingred)

            if ingred == key:
                return key

            elif jw_score >= 0.95:
                return key

            else:
                if split_name_match(key, ingred):
                    return key

    return None


def split_name_match(key, ingred):
    '''
    Figure out how much the words in an ingredient name overlap 
    those in an additive name.

    Inputs: 
        key: (str) key in additives dict 
        ingred: (str) lowercase ingredient name

    Returns: True if it's a match
    '''
    split_ingred = ingred.split()
    ing_set = set(split_ingred)

    rem_parens = re.sub('[()]', '', key)
    split_str = re.split(r"[,\s]\s*", rem_parens)
    add_set = set(split_str)
    
    add_ing_union = ing_set.union(add_set)
    add_ing_intersec = ing_set.intersection(add_set)
    frac = len(add_ing_intersec) / len(add_ing_union)

    if frac > 2/3:
        return True
    