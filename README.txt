CS_122_Quarter_Project

OVERVIEW: Data on food additives was scraped from the FDA website, and 
        ingredient lists for cereal bars, nutrition bars, breakfast bars, etc 
        were scraped from the Jewel Osco website and the Direct Eats website. 
        Products from these stores were assigned health scores based on how 
        many ingredients in them were matched to food additives, as defined 
        by the FDA. Users may interact with a terminal interface to get 
        information about these products and their health scores, helping 
        them make more informed decisions about which products may be 
        healthier than others, based on the additives they contain. 
        
Available Scripts:
        Run "pip install Bullet" if you do not have Bullet already installed
        Run "python3 cli.py" to acess the project's command line interface

-------------------------------------------------------------------------------

FILES:

cli.py: Command line interface to calculate a selected products health score 
        given a selected list of ingredients to ignore. To run, pip install 
        bullet and enter python3 cli.py into the command line. Press the up 
        and down arrow keys to navigate the dropdowns for additives and 
        products. For the additives, press the space bar to select each 
        additive you want to ignore. The interface will also ask you to create 
        an account to store your list of ignored additives for future use, as 
        well as ask if you want to see more information about health score 
        statistics and the additives considered.

algorithm.py: Contains the function calculate_score, which takes in a product 
        name and a list of ingredients to ignore and computes a score based on 
        the amount of addditives there are in the product. It also contains 
        get_stats and final_score, which provide the user with information 
        about their health score in the context of health scores of other 
        products. Additionally, it contains considered_additives, which 
        returns a list of additives that factored into the health score 
        calculation.

fda.py: Contains functions to process the FDA webpage that lists information 
        about food additives. Also creates dictionaries and csv files that map 
        additive names to their categories (e.g., preservative), additive 
        names to unique ids, and category abbreviations to descriptions and 
        unique ids.

adds_to_ids.csv: csv where column 1 is the additive name and column 2 is the 
        unique id (int) for the additive.

categories.csv: csv where column 1 is an FDA category abbreviation 
        (e.g., PRES), column 2 is the description of the category, and 
        column 3 is a unique id (int) for the category.

additives.csv: csv where column 1 is an additive name, and column 2 is a 
        category corresponding to that additive. Additives that map to 
        multiple categories have a row for each category.

ingred_to_additives.py: Contains functions to match ingredient names to 
        additive names from the FDA data. Creates a dictionary mapping product 
        names to lists of tuples of (additive name, original ingredient name). 
        The dict is then writte to a csv, products_to_additives.csv.

products_to_additives.csv: csv where column 1 is a product name, column 2 is 
        the FDA Additive name, and column 3 is the original name of the 
        additive as listed in the product's ingredient list.

jewel_plus_direct.py: Combines the dictionary mapping Jewel Osco products to 
        ingredint lists with the dictionary mapping Direct Eats products to 
        ingredient lists, and writes the combined dict to a csv,
        products_to_ingredients.csv.

products_to_ingredients.csv: csv where column 1 is the product name, column 2 
        is the product's ingredient list, and column 3 is the length of the 
        product's ingredient list (where nested lists are counted as a single 
        entry). 

health.db: sqlite database containing tables corresponding to the csv files 
        with information about products, additives, etc. It also contains 
        tables with user information which allow the program to remember users 
        and their preferences regarding whether they would like to ignore 
        certain additives when calculating health scores for products. 

populate_db.sql: sql code to populate 'products_to_ingredients' table, 
        'products_to_additives' table, 'additives' table, and 'categories' 
        table with data recorded in products_to_ingredients.csv, 
        products_to_additives.csv, adds_to_ids.csv, and categories.csv. 

direct_eats_dict.py: python code to scrape the direct eats website. It starts
        at the first page of the direct eats health bar directory and goes 
        through 13 pages, collecting all the links of every health bar. It then 
        goes through that list of links and scrapes each page for the product 
        name and the ingredient list for that given prodcut. Sublists of 
        ingredients are stored as nested lists and products without ingredients
        are stored as "empty". 

Jewel_Osco_list.py: python code to scrape the Jewel Osco website. The HTML doesn't give 	all product links on a page that are there when you actually visit, so we need to 	start at several different links and pick only unique links. We then loo through 	the list of product pages and return a dictionary mapping product names to a list 	containing two elements: first, a list of ingredients in the product, with 	  	sublists of ingredients stored as nested lists, and second the length of the 	    	aforementioned ingredients list.




