

import sqlite3
import os
import pandas as pd

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'health.db')

db = sqlite3.connect(DATABASE_FILENAME)
c = db.cursor()

def calculate_score(product, ignore_lst):
    '''
    Computes the health score of a product based on the addiitives in the ingredients and their
    positiion in the list of ingredients.

    Inputs:
        product (str): Name of the product within our database
        ignore_lst (list): List of additives that, if present, will not be considered in the health score

    Returns:
        final_ration (float): Health score for the given product and ignore_lst

    '''


    ing_list = c.execute('SELECT ingredient_list FROM products_to_ingred WHERE product_name=?', (product,)).fetchall()
    ing_list = ing_list[0][0]
    ing_list = eval(ing_list)
    additives = c.execute('SELECT orig_ing_name,fda_additive_name FROM products_to_additives WHERE product_name=?', (product,)).fetchall()
    additive_dict = {}
    for i in additives:
        if type(i[0]) == list:
            additive_dict[tuple(i[0])] = i[1]
        else:
            additive_dict[i[0]] = i[1]
    ing_len = len(ing_list)
    bad_score = 0
    for i, ing in enumerate(ing_list):
        if type(ing) == str:
            weight = 1 - (i / ing_len)
            if ing in additive_dict and additive_dict[ing] not in ignore_lst:
                bad_score += weight
        elif type(ing) == list:
            for j in ing:
                weight = (1 - (i / ing_len))/len(ing)
                if j in additive_dict and additive_dict[j] not in ignore_lst:
                        bad_score += weight
    final_ratio = bad_score / len(ing_list)
    return 100*final_ratio

def get_stats(ignore_lst):
    '''
    Computes stats for the entire database of products, with a given list of additives to ignore not 
    factoring into their health scores

    Input(s):
        ignore_lst(list): list of additives to ignore

    Returns:
        stat_dict(dict): dictionary mapping measurement names to their numbers

    '''
    stat_dict={}
    p = c.execute('SELECT product_name FROM products_to_additives')
    product_lst=[]
    score_lst=[]
    for i in p.fetchall():
        if i[0] not in product_lst:
            product_lst.append(i[0])
    total_score=0
    for product in product_lst:
        prod_score=calculate_score(product,ignore_lst)
        total_score+=prod_score
        score_lst.append(prod_score)
    stat_df=pd.DataFrame({'product':product_lst,'score':score_lst})
    quartiles=stat_df.quantile([0.25,0.5,0.75])
    stat_dict['mean']=total_score/len(product_lst)
    stat_dict['first_quartile']=quartiles['score'].iloc[0]
    stat_dict['median']=quartiles['score'].iloc[1]
    stat_dict['third_quartile']=quartiles['score'].iloc[2]
    stat_dict['std']=stat_df['score'].std()
    stat_dict['max']=stat_df['score'].max()
    stat_dict['min']=stat_df['score'].min()
    return stat_dict

stats=get_stats([])
mean=stats['mean']

def final_score_info(product,ignore_lst):
    '''
    Calculates how much the health score for the given product and list of ignored
    additives is relative to the mean
    '''
    score=calculate_score(product,ignore_lst)
    perc_of_avg=score/mean
    return score, perc_of_avg

def counted_additives(product, ignore_lst):
    '''
    Returns a list of the additives that were considered in the computing of a health score,
    based on the additives in the product and the list of ignored additives
    '''
    specific_additives = []
    additives = c.execute('SELECT fda_additive_name FROM products_to_additives WHERE product_name=?', (product,)).fetchall()
    for i in additives:
        if i[0] not in ignore_lst and i[0] not in specific_additives:
            specific_additives.append(i[0])

    return specific_additives