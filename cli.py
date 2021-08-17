from bullet import Bullet, SlidePrompt, Check, Input, YesNo, Numbers, Password, ScrollBar
from bullet import styles
from bullet import colors
from bullet import emojis
import sqlite3
import os
import hashlib
import algorithm


DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'health.db')

db = sqlite3.connect(DATABASE_FILENAME)
c = db.cursor()
r = c.execute('SELECT fda_additive_name FROM products_to_additives')
additive_lst = []
for i in r.fetchall():
    if i[0] not in additive_lst:
        additive_lst.append(i[0])

product_lst = []
p = c.execute('SELECT product_name FROM products_to_additives')
for i in p.fetchall():
    if i[0] not in product_lst:
        product_lst.append(i[0])

valid=True
account = SlidePrompt(
    [
        YesNo("Do you have an account? ",
            default = 'n',
            word_color = colors.foreground["yellow"])])

if not account.launch()[0][1]:
    account_info = SlidePrompt(
    [
        Input("Create username ",
            word_color = colors.foreground["yellow"]),
        Password("Create password ",
            word_color = colors.foreground["yellow"])])


    result = account_info.launch()
    pw = hashlib.sha256(bytes(result[1][1], encoding='utf-8')).hexdigest()
    user = result[0][1]
    c.execute("INSERT INTO users (user_email, user_password) VALUES(?, ?)", (user, pw))
    db.commit()
    product_info = SlidePrompt([
        Check("In general, what additives would you like us to not consider in calculating the product's health score? ",
            choices = additive_lst,
            check = " √",
            margin = 2,
            check_color = colors.bright(colors.foreground["red"]),
            check_on_switch = colors.bright(colors.foreground["red"]),
            background_color = colors.background["black"],
            background_on_switch = colors.background["white"],
            word_color = colors.foreground["white"],
            word_on_switch = colors.foreground["black"])])
    ignore_lst = product_info.launch()[0][1]
    c.execute("INSERT INTO user_info (user_email, ingred_to_ignore) VALUES(?, ?)", (user, str(ignore_lst)))
    db.commit()
else:
    account_info = SlidePrompt(
    [
        Input("Enter username ",
            word_color = colors.foreground["yellow"]),
        Password("Enter password ",
            word_color = colors.foreground["yellow"])])
    result = account_info.launch()
    user = result[0][1]
    pw = hashlib.sha256(bytes(result[1][1], encoding='utf-8')).hexdigest()
    if (user, pw) in c.execute('SELECT * FROM users WHERE user_email = ? AND user_password = ?;', (user, pw)).fetchall():
        account_prefs = SlidePrompt([
        YesNo('Would you like to change your list of ignored additives?',
            default = 'n',
            word_color = colors.foreground["yellow"])])
        change = account_prefs.launch()
        if change[0][1]:
            new_prefs = SlidePrompt([
            Check("In general, what ingredients would you like us to not consider in calculating the product's health score?(Press space to select) ",
            choices = additive_lst,
            check = " √",
            margin = 2,
            check_color = colors.bright(colors.foreground["red"]),
            check_on_switch = colors.bright(colors.foreground["red"]),
            background_color = colors.background["black"],
            background_on_switch = colors.background["white"],
            word_color = colors.foreground["white"],
            word_on_switch = colors.foreground["black"])])
            ignore_lst = new_prefs.launch()[0][1]
            c.execute('DELETE FROM user_info WHERE user_email = ?', (user,))
            db.commit()
            c.execute("INSERT INTO user_info (user_email, ingred_to_ignore) VALUES(?, ?)", (user, str(ignore_lst)))
            db.commit()
        else:
            ignore_lst = c.execute('SELECT ingred_to_ignore FROM user_info WHERE user_email = ?', (user,)).fetchall()
            ignore_lst = eval(ignore_lst[0][0])
    else:
        valid = False
        print('Invalid user or password')
if valid:
        product_info = SlidePrompt([ScrollBar("What product are you looking for? ",
            choices = product_lst,
            height = 20,
            align = 5,
            margin = 0,
            pointer = "👉",
            background_color = colors.background["black"],
            background_on_switch = colors.background["white"],
            word_color = colors.foreground["white"],
            word_on_switch = colors.foreground["black"])])
        product=product_info.launch()[0][1]
        score = algorithm.final_score_info(product, ignore_lst)
        print('Your health score for this product is ' + str(round(score[0],2)) + '. \nYour product\'s health score is ' + str(round(score[1]*100,2)) + \
        ' percent of the mean health score in our database, or ' + str(round(score[1],4))+ \
        ' times the mean. Note that smaller health scores indicate healthier products that have less harmful additives')

        more_stats = SlidePrompt([YesNo("Would you like to see more statistics on your product?",
            default = 'n',
            word_color = colors.foreground["yellow"])])
        wants_stats = more_stats.launch()[0][1]
        if wants_stats:
            stats=algorithm.get_stats(ignore_lst)
            print('Given your list of ignored additives, the mean health score was '+ str(round(stats['mean'],2))\
            + ', \nthe first quartile was ' + str(round(stats['first_quartile'],2))\
            + ', \nthe median was ' + str(round(stats['median'],2))\
            + ', \nthe third quartile was ' + str(round(stats['third_quartile'],2))
            + ', \nthe standard deviation was ' + str(round(stats['std'],2))
            + ', \nthe max was ' + str(round(stats['max'],2))
            + ', \n and the min was ' + str(round(stats['min'],2)) + '.')
        
        personal_additives = SlidePrompt([YesNo("Would you like to see the additives in this product that factored into your health score?",
            default = 'n',
            word_color= colors.foreground['yellow'])])
        wants_additives = personal_additives.launch()[0][1]
        if wants_additives:
            counted_additives = algorithm.counted_additives(product, ignore_lst)
            print('These were the additives that factored into the calculation of your health score:' + str(counted_additives))

          
        repeat = SlidePrompt([YesNo('Do you want continue', 
                         default='n',
                         word_color = colors.foreground["yellow"])])

        while repeat.launch()[0][1]:
            account_prefs = SlidePrompt([
            YesNo('Would you like to change your list of ignored additives?',
            default = 'n',
            word_color = colors.foreground["yellow"])])
            change = account_prefs.launch()
            if change[0][1]:
                new_prefs = SlidePrompt([
                Check("In general, what ingredients would you like us to not consider in calculating the product's health score?(Press space to select) ",
                choices = additive_lst,
                check = " √",
                margin = 2,
                check_color = colors.bright(colors.foreground["red"]),
                check_on_switch = colors.bright(colors.foreground["red"]),
                background_color = colors.background["black"],
                background_on_switch = colors.background["white"],
                word_color = colors.foreground["white"],
                word_on_switch = colors.foreground["black"])])
                ignore_lst = new_prefs.launch()[0][1]
                c.execute('DELETE FROM user_info WHERE user_email = ?', (user,))
                db.commit()
                c.execute("INSERT INTO user_info (user_email, ingred_to_ignore) VALUES(?, ?)", (user, str(ignore_lst)))
                db.commit()
            else:
                ignore_lst = c.execute('SELECT ingred_to_ignore FROM user_info WHERE user_email = ?', (user,)).fetchall()
                ignore_lst = eval(ignore_lst[0][0])


            product_info = SlidePrompt([ScrollBar("What product are you looking for? ",
                choices = product_lst,
                height = 20,
                align = 5,
                margin = 0,
                pointer = "👉",
                background_color = colors.background["black"],
                background_on_switch = colors.background["white"],
                word_color = colors.foreground["white"],
                word_on_switch = colors.foreground["black"])])
            product=product_info.launch()[0][1]
            score = algorithm.final_score_info(product, ignore_lst)
            print('Your health score for this product is ' + str(round(score[0],2)) + '. \nYour product\'s health score is ' + str(round(score[1]*100,2)) + \
            ' percent of the mean health score in our database, or ' + str(round(score[1],4))+ \
            ' times the mean. Note that smaller health scores indicate healthier products that have less harmful additives')

            more_stats = SlidePrompt([YesNo("Would you like to see more statistics on your product?",
                default = 'n',
                word_color = colors.foreground["yellow"])])
            wants_stats = more_stats.launch()[0][1]
            if wants_stats:
                stats=algorithm.get_stats(ignore_lst)
                print('Given your list of ignored additives, the mean health score was '+ str(round(stats['mean'],2))\
                + ', \nthe first quartile was ' + str(round(stats['first_quartile'],2))\
                + ', \nthe median was ' + str(round(stats['median'],2))\
                + ', \nthe third quartile was ' + str(round(stats['third_quartile'],2))
                + ', \nthe standard deviation was ' + str(round(stats['std'],2))
                + ', \nthe max was ' + str(round(stats['max'],2))
                + ', \n and the min was ' + str(round(stats['min'],2)) + '.')
            
            personal_additives = SlidePrompt([YesNo("Would you like to see the additives in this product that factored into your health score?",
                default = 'n',
                word_color= colors.foreground['yellow'])])
            wants_additives = personal_additives.launch()[0][1]
            if wants_additives:
                counted_additives = algorithm.counted_additives(product, ignore_lst)
                print('These were the additives that factored into the calculation of your health score:' + str(counted_additives))
                
            repeat = SlidePrompt([YesNo('Do you want continue', 
                         default='n',
                         word_color = colors.foreground["yellow"])])        



