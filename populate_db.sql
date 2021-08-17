DROP TABLE IF EXISTS additives;
CREATE TABLE additives(
    additive_name TEXT NOT NULL,
    additive_id INT
);
.mode csv additives
.import adds_to_ids.csv additives

DROP TABLE IF EXISTS categories;
CREATE TABLE categories(
    cat_abbrev TEXT NOT NULL,
    cat_desc TEXT NOT NULL,
    cat_id INT
);
.mode csv categories
.import categories.csv categories

DROP TABLE IF EXISTS products_to_additives;
CREATE TABLE products_to_additives(
    product_name TEXT NOT NULL,
    fda_additive_name,
    orig_ing_name
);
.mode csv products_to_additives
.import products_to_additives.csv products_to_additives

DROP TABLE IF EXISTS products_to_ingred;
CREATE TABLE products_to_ingred(
    product_name TEXT NOT NULL,
    ingredient_list,
    num_ingredients INT
);
.mode csv products_to_ingred
.import products_to_ingred.csv products_to_ingred