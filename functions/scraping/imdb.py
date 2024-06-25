import requests
from bs4 import BeautifulSoup
import re


def find_url(game):
    """
    Search on google the imdb site for an specific game
    
    """
    
    game = re.sub(' ', '+',game) + "+game+imdb"
    link = f"https://www.google.com.br/search?q={game}" #search
    page = requests.get(link)
    soup = BeautifulSoup(page.text,"lxml")
    fatia = soup.find("div", class_="egMi0 kCrYT") #extract the best result
    link = fatia.find("a")
    link = link['href'] #gets the link
    #link = re.search(r'/url\?q=(.+?)&sa=',link).group(1) #filters only the good part
    game_imdb_id = link.split('/')[5]
    link = f"https://www.imdb.com/title/{game_imdb_id}"
    return(link)    #return the main link
    
def info_person(person):
    """
    recives an commentary and extracts all the information needed
    
    """
    
    personal_list=[]
    title = re.sub(';','.', person.find("a", class_="title").text.strip())
    comment = re.sub(';','.',person.find("div", class_="text show-more__control").text.strip()) #gets the commentary part 
    comment= re.sub(r'\s+', ' ', comment)#cleans the commentary
    comment = re.sub(r'\n', ' ',comment)#cleans it even more
    
    try:
        rate = person.find("span", class_="rating-other-user-rating").text.strip() #gets the rate of the person, if it does not work, the person did not gave us an final rate
        rate = rate.split('/')[0]
    except:
        rate = '5' 
        
    date = person.find("span", class_="review-date").text.strip()
    
    people_opinion = person.find("div", class_="actions text-muted").text.strip().split('  ')[0]
    
    #Now we append all the information of the person we just got
    personal_list.append(title)
    personal_list.append(comment)
    personal_list.append(rate)
    personal_list.append(date)
    personal_list.append(people_opinion)
    
    return personal_list #returns the person list 

def find_genre_and_description(link_main):
    print(link_main)
    page = requests.get(link_main,
                        headers = {
                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
                            })
    soup = BeautifulSoup(page.text,'lxml')
    try:
        genre = soup.find('span', class_="ipc-chip__text").text.strip()
    except:
        print('genre',link_main)
    try:
        description = soup.find("span", class_="sc-96357b74-2 CKcbM").text
        description = re.sub(';','.',description)
    except:
        print('description', link_main)
        
    return genre, description

def search_for_game_information(game):
    """
    recives an game and extracts the data from it
    
    """
    link_main = find_url(game)
    link_comments = link_main + "/reviews/?ref_=tt_ov_rt" #gets the commentary link of that game
    page = requests.get(link_comments) 
    soup = BeautifulSoup(page.text, "lxml")
    genre,description= find_genre_and_description(link_main)
    
    people_info = soup.find_all("div", class_="lister-item mode-detail imdb-user-review collapsable") #gets all the commentaries available on the page
    game_list = [genre,description] #contém os comentários de um certo jogo
    count = 1
    #Para cada comentário irá se extrair os dados:
    for person in people_info:
        if(count>20): #if the count exceed 20, it will not search for more
            break
        #Here we extract everything from an commentary:
        personal_list = info_person(person) #contain information, in this order[title,commentary,rate,date,people_opinion]
        game_list.append(personal_list) #appends the information we just got 
        count+=1    
        
    return game_list #returns all the commentaries we got on a list  [genre,description,comment1,comment2,...]
                
def search_for_company_games(info,company_id,game_id):
    """
    Search for the information of each game in the company
    """
    #'info' is on this format:Company1||||big_game_1||||big_game_2||||big_game_3||||recent_game_1||||recent_game_2
    info = info.split('||||') #Transform the string in a list, so we can extract the information 
    company= info[0]
    games = info[1:]
    commentaries_list_company = [company]
    
    with open('data/imdb_companies.csv','a',encoding='utf-8') as file:
        file.write(f'{company_id};{company}\n')
    
    
    for game in games: #for each game of the company, it will extract the data needed 
        commentaries_list_company.append([game_id,search_for_game_information(game),company_id,game]) #calls the function search_for_game_information() 
        game_id+=1
    write(commentaries_list_company) #calls the function write
    
    return game_id #returns the current game_id number so we can keep track of the position we are
    
def write(commentaries_list_company):
    """
    This function is used to write the data on an .csv file    
    """
    
    with open('data/imdb_game_company.csv','a',encoding = 'utf-8') as file:
        for _game_ in commentaries_list_company[1:]: #for each information in the list, it will write it on the .csv file
            game_id = _game_[0] # catch the game
            company_id = _game_[2]
            game_name = _game_[3]
            description = _game_[1][1]
            file.write(f'{game_id};{game_name};{company_id};{description}\n')
    
    with open('data/imdb_game.csv', 'a', encoding = 'utf-8') as file:
        for _game_ in commentaries_list_company[1:]: #for each information in the list, it will write it on the .csv file    
            
            game_id = _game_[0] # catch the game
            genre = _game_[1][0]
            lista = _game_[1] #cath the info about the game
            for person in lista[2:]: #for each person that commented on the game:
                file.write(f"{game_id};{genre};{person[0]};{person[1]};{person[2]};{person[3]};{person[4]}")

def imdb():    
    """
    This Function do all the work needed in order to get the data from imdb
    """
    
    with open('data/imdb_companies.csv', 'w', encoding='utf-8') as file:
        file.write('COMPANY ID;COMPANY NAME\n')
    
    with open('data/imdb_game_company.csv','w',encoding = 'utf-8') as file:
        file.write('GAME ID;GAME NAME; COMPANY ID;DESCRIPTION\n')
    
    with open('data/imdb_game.csv', 'w',encoding='utf-8') as arquivo:
        arquivo.write("GAME_ID;GENRE;COMMENTARY TITLE;COMMENTARY;RATE;DATE;GENERAL OPINION ABOUT THE COMMENTARY"+"\n") #Every time the program starts, it will crate an new file
    
    with open('data/steam_list.csv','r',encoding = 'utf-8') as arquivo: #Opens the file that contains all the information required in order to start the program
        company_id = 0
        game_id = 0
        for info in arquivo:
            print("======== PEGANDO DO IMDB ========")
            print(company_id)
            game_id = search_for_company_games(info.strip(),company_id,game_id) #Do the work for each line
            company_id+=1

