'''
This module we'll collect games info that are on Steam 
'''

import requests
from bs4 import BeautifulSoup
import re
import time


def google_search(game):
    """
    Here we search a game on google and takes the valid Steam link
    """

    #https://www.bing.com/search?q=dead+by+daylight+steam
    game = re.sub(' ','+', game)   # replace the blank spaces for +
    url_google = f"https://www.google.com/search?q={game}steam"
    page = requests.get(url_google)
    soup = BeautifulSoup(page.text,"lxml")
    slices = soup.find_all("div", class_="egMi0 kCrYT")

    for s_slice in slices:    
        try:
            link = s_slice.find("a")
            link = link['href']
            game_id = re.search(r'/app/(\d+)', link).group(1)                    
            link = f"https://store.steampowered.com/app/{game_id}"
            #print(link)
            return [game_id,link]   # return the Steam game link to the code
        except:
            continue
   

def adjust_date(date):
    """
    Here we fix the date format. It comes like this: Posted : date (with a comma and some without the year number) 
    """

    date = re.search(r'Posted: (.+)',date).group(1)  # take the date
    date = re.sub(',', '',date)   # cut the comma
    
    cont = 0
    for i in date:
        if i == ' ':
            cont+=1
    if cont == 1:
        date = date + " 2024"  # in case the year doesn't appear, we add '2024'
    
    day = int(date[0:2])
    rest = date[2:].strip()  #  function 'rest' contains everything that isn't the day number
    year = rest[-4:]
    months_dict = {'January': '01',
                   'February': '02',
                   'March':'03',
                   'April':'04',
                   'May':'05',
                   'June':'06',
                   'July':'07',
                   'August':'08',
                   'September':'09',
                   'October':'10',
                   'November':'11',
                   'December':'12'}
    month = rest[:-4].strip()
    month = months_dict[month]
    date = f'{day}/{month}/{year}'
    
    return date


def adjust_opinions(opinions):
    """
    Function to fix and format the reviews. 
    """
    
    # each comment has up to 4 types: helpful-funny(1), helpful(2), funny(3) and, neither(4):

    if opinions == 'N/I':  # case 4
        return ['0', '0'] 
    option = opinions.split('\t')[0]
    #print('---------',opinions)

    if 'helpful' and 'funny' in opinions:  # case 1 
        try:
            opinions = re.search(r'(.+) people found this review helpful(.+) people found this review funny',option)
            helpful = opinions.group(1)
            funny = opinions.group(2)
            return [helpful, funny]
        except:
            opinions = re.search(r'(.+) people',option)
            helpful = opinions.group(1)
            funny = 1
            return [helpful, funny]
            
    if 'helpful' in opinions:  # case 2
        try: 
            opinions = re.search(r'(.+) people found this review helpful',option)
            helpful = opinions.group(1)
            return [helpful,'0']
        except:
            opinions = re.search(r'(.+) person found this review helpful',option)
            helpful = opinions.group(1)
            return [helpful,'0']

    if 'funny' in opinions:  #case 3
        try:
            opinions = re.search(r'(.+) people found this review funny',option)
            funny = opinions.group(2)
            return ['0', funny]
        except:
            opinions = re.search(r'(.+) person found this review funny',option)
            funny = opinions.group(2)
            return ['0', funny]


def  collect_data(person):
    """
    Here we collect info about a especific comment
    """
    
    # collecting:
    date = person.find("div", class_="date_posted").text.strip()
    hours = person.find("div", class_="hours").text.strip()  # it is on this format: '{hours} hrs on record'
    comment = person.find("div", class_="apphub_CardTextContent").text.strip() # take a large block of code that contains the date and the comment
    final_opinion = person.find("div", class_="title").text.strip()
    try:
        opinions = person.find("div", class_="found_helpful").text.strip()
    except:
        opinions = "N/I"
        
    # cleaning:
    date = adjust_date(date)  # clean the date number
    hours= re.search(r'(.+) hrs on record',hours).group(1)  # clean the hour number
    comment = re.search(r'Posted: (.+)\n(.+)',comment).group(2).strip()  # take only the comment
    comment = re.sub(';', '.', comment)  # replace ';' for '.' to avoid formatting errors on Excel
    helpful,funny = adjust_opinions(opinions)
    hours = re.sub(',','',str(hours))
    hours = re.sub(r'\.',',',hours)
    helpful = re.sub(',','', str(helpful))
    funny = re.sub(',','',str(funny))
    if final_opinion == 'Recommended':
        final_opinion = 1
    else:
        final_opinion = 0
    
    
    return [comment, final_opinion, hours, date, helpful, funny]  # return a list in the specified order we want
    

def collect_comments(link_main, game_id):
    """
    Here we collect the comments infos about a game
    """
    
    link_comments = f"https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated&snr=1_5_100010_"  # the link
    page = requests.get(link_comments)
    soup = BeautifulSoup(page.text, "lxml")
    comments = soup.find_all("div",  class_="apphub_UserReviewCardContent")  # take all the comments and create a list
    data_comments = []  # list that will keep all the collected comments

    for person in comments:  # for each comment, collect and clean
        dados_comment = collect_data(person)  # collect the data on a list
        data_comments.append(dados_comment)
    
    return data_comments


def collect_price(values_table):
    """
    Here we'll collect the price of a specific game, caring about the discount and the whole price
    """

    try:  # desconsidering the discount:
        temp = []
        prices = values_table.find_all("div", class_="game_purchase_price price")
        for price_game in prices:
            print(price_game.text.strip())
            if 'Free' in price_game.text.strip():
                return '00,00'
            if 'DEMO' in price_game.text.strip():
                continue
            if '$' not in price_game.text.strip():
                continue
            temp.append(price_game)
            if len(temp) != 0:
                return price_game.text.strip()[2:]
            a = price_game.group(1)
            print("!"*50)
        prices.group('1') #if it pass through all the if's and still got 'None', then we force an error to happen  
        
    except:
        try:  # considering that the game has the discount:
            sentence = values_table.find("div", class_="discount_block game_purchase_discount").text  # take a phrase with the discount and the final price
            discount = values_table.find("div", class_="discount_pct").text.strip()[1:]
            price_original = values_table.find("div", class_="discount_original_price").text.strip()
            price_final = values_table.find("div", class_="discount_final_price").text.strip()
            
            return price_final[3:]
        except:
            try:  # considering that there is a discount on the price for buying DLCs:
                price_final = values_table.find("div", class_="discount_final_price").text[2:]
                price_final = re.sub(',','.',price_final)  # take out the commas
                price_final = re.sub(' ','',price_final)  # take out the blank spaces
                discount = values_table.find("div", class_="bundle_base_discount").text.strip()[1:-1]
                discount = re.sub(' ', '',discount)  # take out blank spaces, again
                discount = float(discount)/100
                price_final = float(price_final)
                price_original = price_final/(1-discount)

                return(price_original[2:])
            except:
                try:
                    preco = values_table.find("div", class_="discount_final_price").text.strip()
                    print(preco)
                    return preco[2:]
                except:    
                    return "00,00"
        
   
def collect_gender(soup):
    """
    Here we collect the game category
    """

    try:
        table = soup.find("div", class_="details_block")  # take some infos
        gender = re.search(r'Genre:(.+)\n',table.text).group(1).strip() # take the game category
        gender = gender.split(',')[0] #cleaning and only extracting the first genre of the list
        return gender
    except:
        try:
            table = soup.find("div", class_="block_content_inner")
            gender = re.search(r'Genre:(.+)\n',table.text).group(1).strip()
            gender = gender.split(',')[0]
            return gender
        except:
            print("gender")
            
def collect_requirements(soup):
    try: #The game has minimum and recommended requirements
        #collecting:         
        minimum_requirements= soup.find("div", class_="game_area_sys_req_leftCol").text.strip()
        recommended_requirements= soup.find("div", class_="game_area_sys_req_rightCol").text.strip()
       
        #cleaning the data:
        minimum_requirements = re.sub(';','.',minimum_requirements).split('\n\n')[0] #removes all ';' and gets only the part before \n\n
        recommended_requirements = re.sub(';','.',recommended_requirements).split('\n\n')[0] #removes all ';' and gets only the part before \n\n
        
        minimum_requirements = minimum_requirements.split('Minimum:')[1]
        recommended_requirements = recommended_requirements.split('Recommended:')[1]
        
        return minimum_requirements, recommended_requirements #returns the requirements
    except:
        try: #The game has only the minimum requirements
            #collecting the data    
            minimum_requirements = soup.find("div", class_="game_area_sys_req sysreq_content active").text.strip()
            
            #cleaning the data:
            minimum_requirements=re.sub(';','.',minimum_requirements).split('\n\n')[0]
                   
            minimum_requirements = minimum_requirements.split('Minimum:')[1]
            
            return minimum_requirements,'NOT INFORMED' #return the requirement
        except:
            try: #Another type of requirements on the game: 
                #collecting the data:
                minimum_requirements = soup.find("div", class_="game_area_sys_req_full").text.strip()
                #cleaning the data:
                    
                minimum_requirements = re.sub(';','.',minimum_requirements).split('\n\n')[0]
                return minimum_requirements,'NOT INFORMED'
            except:
                
                #if it does not find an requirement on the page, it will return 'NOT INFORMED'
                return('NOT INFORMED','NOT INFORMED')
                
def collect_game_information(game):
    """
    Here we collect the infos about a game
    """
    
    game_id,link_main = google_search(game)  # take the game's home page link on Steam and his id
    page = requests.get(link_main)
    print("======== PEGANDO DA STEAM ========")
    print(game.strip(),'---',link_main)
    soup = BeautifulSoup(page.text,"lxml")
    gender = collect_gender(soup)
    data_comments = collect_comments(link_main,game_id)  # collect the comments about the game
    values_table = soup.find("div", class_="game_area_purchase")
    price_game = collect_price(values_table)
    minimum_requirements, recommended_requirements = collect_requirements(soup)
    return gender, data_comments,price_game,minimum_requirements,recommended_requirements


def steam():
    #restarting all the csv's:
    
    with open('data/steam_games.csv', 'w', encoding = 'utf-8') as file_steam_games: 
        file_steam_games.write('GAME ID;CATEGORY;PRICE;COMMENT;FINAL OPINION;HOURS SPENT;DATE OF THE COMMENT; HELPFUL; FUNNY;\n')
    
    with open('data/steam_companies.csv','w', encoding='utf-8') as file:
        file.write('COMPANY ID; COMPANY\n') 
    
    with open('data/steam_game_company.csv','w',encoding = 'utf-8') as file:
        file.write('GAME ID;GAME NAME;GAME COMPANY ID;MINIMUM REQUIREMENTS; RECOMMENDED REQUIREMENTS\n')
    
    with open('data/steam_list.csv','r',encoding = 'utf-8') as file_steam_list:
        game_id = -1
        for company_id,line in enumerate(file_steam_list):  # each line is in this format : 'Epic Games||||Fortnite||||Gears of War||||Infinity Blade||||Fortnite Chapter 2 Season 8||||Tony Hawk's Pro Skater 1+2'

            s_list = line.split('||||')
            enterprise = s_list[0].strip()
            print('\n\n',enterprise)
            
            for game in (s_list[1:]):
                game_id += 1
                
            
                
                try:
                    gender, data_comments, price_game,minimum_requirements,recommended_requirements = collect_game_information(game)
                    to_write(game_id,company_id,game.strip(),gender,price_game,data_comments,minimum_requirements,recommended_requirements)
                except Exception as error:
                    print('#############',error)
                    
            with open('data/steam_companies.csv','a',encoding = 'utf-8') as file:
                file.write(f'{company_id};{enterprise}\n')


def to_write(game_id,company_id,game,gender,price_game,data_comments,minimum_requirements,recommended_requirements):
    
    #writing on the steam_game_company.csv, so we can search fo an game end its company:
    with open('data/steam_game_company.csv', 'a', encoding = 'utf-8') as file:
        file.write(f'{game_id};{game.strip()};{company_id};{minimum_requirements};{recommended_requirements}\n')
    
    with open('data/steam_games.csv', 'a', encoding = 'utf-8' ) as file:
        for info in data_comments:
            # comment, final opinion, hours, date, helpful, funny
            file.write(f'{game_id};{gender};{price_game};{info[0]};{info[1]};{info[2]};{info[3]};{info[4]};{info[5]}\n')
