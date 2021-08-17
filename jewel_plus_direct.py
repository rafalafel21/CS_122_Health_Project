import csv
import Jewel_Osco_list as jw
import direct_eats_dict as de

jewel_dict=jw.get_ingredient_dicts()
direct_dict=de.crawl_store()

def merge_them():
    '''
    Combine dict of Jewel Osco products with dict of Direct Eats products
    and return the combined dict
    '''
    final_dict=jewel_dict.copy()
    for key, value in direct_dict.items():
        if key not in final_dict.keys():
            final_dict[key]=value
    return final_dict

def dict_to_csv(final_dict):
    '''
    Write combined dict of Jewel Osco products and Direct Eats products to csv
    '''
    with open('products_to_ingred.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, val in final_dict.items():
            writer.writerows([[key] + val])
