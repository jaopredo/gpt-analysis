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
    link = re.search(r'/url\?q=(.+?)&sa=',link).group(1) #filters only the good part
    return(link+"reviews/?ref_=tt_ov_rt")    #return the review link
    
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
    except:
        rate = "Not Informed" 
        
    date = person.find("span", class_="review-date").text.strip()
    
    people_opinion = person.find("div", class_="actions text-muted").text.strip().split('  ')[0]
    
    #Now we append all the information of the person we just got
    personal_list.append(title)
    personal_list.append(comment)
    personal_list.append(rate)
    personal_list.append(date)
    personal_list.append(people_opinion)
    
    return personal_list #returns the person list 

def search_for_game_information(game):
    """
    recives an game and extracts the data from it
    
    """
    
    link = find_url(game) #gets the commentary link of that game
    page = requests.get(link) 
    soup = BeautifulSoup(page.text, "lxml")
    
    people_info = soup.find_all("div", class_="lister-item mode-detail imdb-user-review collapsable") #gets all the commentaries available on the page
    game_list = [] #contém os comentários de um certo jogo
    count = 1
    #Para cada comentário irá se extrair os dados:
    for person in people_info:
        if(count>20): #if the count exceed 20, it will not search for more
            break
        #Here we extract everything from an commentary:
        personal_list = info_person(person) #contain information, in this order[title,commentary,rate,date,people_opinion]
        game_list.append(personal_list) #appends the information we just got 
        count+=1    
        
    return game_list #returns all the commentaries we got on a list

def write(commentaries_list_company):
    """
    This function is used to write the data on an .csv file    
    """
    
    with open('dados/imdb.csv', 'a', encoding = 'utf-8') as file:
        company = commentaries_list_company[0]
        for _game_ in commentaries_list_company[1:]: #for each information in the list, it will write it on the .csv file
            game = _game_[0] # catch the game
            lista = _game_[1] #cath the info about the game
            for person in lista: #for each person that commented on the game:
                file.write(f"{company};{game};{person[0]};{person[1]};{person[2]};{person[3]};{person[4]}")
                
def search_for_company_games(info):
    """
    Search for the information of each game in the company
    """
    
    #'info' is on this format:Company1||||big_game_1||||big_game_2||||big_game_3||||recent_game_1||||recent_game_2
    info = info.split('||||') #Transform the string in a list, so we can extract the information 
    company= info[0]
    games = info[1:]
    commentaries_list_company = [company]
    for game in games: #for each game of the company, it will extract the data needed 
        commentaries_list_company.append([game,search_for_game_information(game)]) #calls the function search_for_game_information() 
    write(commentaries_list_company)

def imdb():    
    """
    This Function do all the work needed in order to get the data from imdb
    """
    
    with open('dados/imdb.csv', 'w',encoding='utf-8') as arquivo:
        arquivo.write("COMPANY;GAME;COMMENTARY TITLE;COMMENTARY;RATE;DATE;GENERAL OPINION ABOUT THE COMMENTARY"+"\n") #Every time the program starts, it will crate an new file
    
    with open('dados/lista_de_pesquisa.csv','r',encoding = 'utf-8') as arquivo: #Opens the file that contains all the information required in order to start the program
        i=1
        for info in arquivo:
            search_for_company_games(info.strip()) #Do the work for each line
            i+=1
            
imdb()