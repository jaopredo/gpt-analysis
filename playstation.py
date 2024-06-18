"""

Pega os dados da playstation e os limpa

"""
import requests
from bs4 import BeautifulSoup
#import os
import re


#os.system("cls")


def links_playstation(url):    
    while(True):
        page = requests.get(url) #pega o conteúdo do site
        soup = BeautifulSoup(page.text, "lxml") #deixa o conteúdo acessível para o BeautifulSoup
        #pegando os links de cada jogo:
        bolo = soup.find_all("ul", class_="psw-grid-list psw-l-grid") #Pega a secção com os catálogos de jogos do momento
        links = []
        for pedaco in bolo:
            parte = pedaco.find_all("a", class_="psw-link psw-content-link") #pega a parte com todos os links
            for link in parte:
                links.append("https://store.playstation.com"+link.get('href')) # Para cada jogo, haverá uma grande quantidade de informação, somente nos interessa a parte com 'href'
        if(links != []):
            #returns the links of all the games 
            return links
                
def informacoes_playstation(link):
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "lxml")
        try:                
            titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-8 psw-l-line-break-word").text.strip() #pega o título do jogo
            description = soup.find("p",class_="psw-c-t-2 psw-p-x-7 psw-p-y-6 psw-p-x-6@below-tablet-s psw-m-sub-x-7 psw-m-auto@below-tablet-s psw-c-bg-card-1").text.strip()           
            informations = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip() #gets some information from the game (publisher, platform,realese date)
            platform = re.search(r'Platform:(.+)Release',informations).group(1) #extracts the Platform
            realese_date = re.search(r'Release:(\d+\/\d+\/\d+)Publisher',informations).group(1)
            publisher = re.search(r'Publisher:(.+)Genres',informations).group(1)
            genres = re.search(r'Genres:(.+)Voice',informations).group(1).split(',')
            languages = re.search(r'Voice:(.+)',informations).group(1).split(',')
            texto = soup.find("div", class_="psw-c-bg-card-1 psw-l-w-1/1 psw-l-w-1/1@tablet-s psw-l-w-7/12@tablet-l psw-l-w-2/3@laptop psw-l-w-2/3@desktop psw-l-w-2/3@max psw-p-6 psw-p-y-6").text.strip()#Pega toda a tabela com as informações das avaliações
            total_avaliadores = re.search(r'from (\d+) ratings', texto).group(1) # pega o total de avaliadores    
            total_estrelas = re.search(r'(\d+\.\d+) stars', texto).group(1) #pega o total de estrelas
            stars = [] #cria uma lista com a porcentagem de avaliação de cada estrela na ordem crescente:1-5
            stars.append(re.search(r'One star(\d+\%)',texto).group(1))#search on the text the pattern
            for i in range(2,6):
                stars.append(re.search(rf'{i} stars(\d+\%)', texto).group(1))#search on the text the pattern described
        
            #returns an dictionary with all the information needed  
            print("Método 1",end = " ")
            return{
                'platform':platform,
                'languages': languages,
                'genres' : genres,
                'realese_date':realese_date,
                'publisher' : publisher,
                'description' : description,
                'title' : titulo, 
                'estrelas' : total_estrelas, 
                'total_avaliadores': total_avaliadores,
                'stars' : stars
                } 
        
        except:
            try:  #Sem availiações do jogo
                titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-7 psw-l-line-break-word").text.strip() #pega o título do jogo               
                description = soup.find("p",class_="psw-c-t-2 psw-p-x-7 psw-p-y-6 psw-p-x-6@below-tablet-s psw-m-sub-x-7 psw-m-auto@below-tablet-s psw-c-bg-card-1").text.strip()                   
                informations = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip() #gets some information from the game (publisher, platform,realese date)                   
                platform = re.search(r'Platform:(.+)Release',informations).group(1) #extracts the Platform                   
                realese_date = re.search(r'Release:(\d+\/\d+\/\d+)Publisher',informations).group(1)                  
                publisher = re.search(r'Publisher:(.+)Genres',informations).group(1)                  
                genres = re.search(r'Genres:(.+)Voice',informations)               
                languages = re.search(r'Voice:(.+)',informations)                 
                texto = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip()#Pega toda a tabela com as informações das avaliações                   
                total_avaliadores = re.search(r'from (\d+) ratings', texto).group(1) # pega o total de avaliadores                     
                total_estrelas = re.search(r'(\d+\.\d+) stars', texto).group(1) #pega o total de estrelas
                stars = [] #cria uma lista com a porcentagem de avaliação de cada estrela na ordem crescente:1-5              
                stars.append(re.search(r'One star(\d+\%)',texto).group(1))#search on the text the pattern
  
                print("Método 2", end = " ")
                #returns an dictionary with all the information needed    
                return{
                    'platform':platform,
                    'languages': languages,
                    'genres' : genres,
                    'realese_date':realese_date,
                    'publisher' : publisher,
                    'description' : description,
                    'title' : titulo, 
                    'estrelas' : total_estrelas, 
                    'total_avaliadores': total_avaliadores,
                    'stars' : stars
                    } 
            except:#outra opção de modelo
                try:    
                    titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-8 psw-l-line-break-word").text.strip() #pega o título do jogo
                    description = soup.find("p",class_="psw-c-t-2 psw-p-x-7 psw-p-y-6 psw-p-x-6@below-tablet-s psw-m-sub-x-7 psw-m-auto@below-tablet-s psw-c-bg-card-1").text.strip()
                    informations = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip() #gets some information from the game (publisher, platform,realese date)
                    platform = re.search(r'Platform:(.+)Release',informations).group(1) #extracts the Platform
                    realese_date = re.search(r'Release:(\d+\/\d+\/\d+)Publisher',informations).group(1)
                    publisher = re.search(r'Publisher:(.+)Genres',informations).group(1)
                    genres = re.search(r'Genres:(.+)Voice',informations)
                    languages = re.search(r'Voice:(.+)',informations)
                    texto = soup.find("div", class_="psw-c-bg-card-1 psw-l-w-1/1 psw-l-w-1/1@tablet-s psw-l-w-7/12@tablet-l psw-l-w-2/3@laptop psw-l-w-2/3@desktop psw-l-w-2/3@max psw-p-6 psw-p-y-6").text.strip()#Pega toda a tabela com as informações das avaliações
                    total_avaliadores = re.search(r'from (\d+) ratings', texto).group(1) # pega o total de avaliadores    
                    total_estrelas = re.search(r'(\d+\.\d+) stars', texto).group(1) #pega o total de estrelas
                    stars = [] #cria uma lista com a porcentagem de avaliação de cada estrela na ordem crescente:1-5
                    stars.append(re.search(r'One star(\d+\%)',texto).group(1))#search on the text the pattern
                    #returns an dictionary with all the information needed    
                    print("Método 3", end = " ")
                    return{
                        'platform':platform,
                        'languages': languages,
                        'genres' : genres,
                        'realese_date':realese_date,
                        'publisher' : publisher,
                        'description' : description,
                        'title' : titulo, 
                        'estrelas' : total_estrelas, 
                        'total_avaliadores': total_avaliadores,
                        'stars' : stars
                        }  
                except:
                    try:
                        titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-6 psw-l-line-break-word").text.strip() #pega o título do jogo
                        description = soup.find("p",class_="psw-c-t-2 psw-p-x-7 psw-p-y-6 psw-p-x-6@below-tablet-s psw-m-sub-x-7 psw-m-auto@below-tablet-s psw-c-bg-card-1").text.strip()
                        informations = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip() #gets some information from the game (publisher, platform,realese date)
                        platform = re.search(r'Platform:(.+)Release',informations).group(1) #extracts the Platform
                        realese_date = re.search(r'Release:(\d+\/\d+\/\d+)Publisher',informations).group(1)
                        publisher = re.search(r'Publisher:(.+)Genres',informations).group(1)
                        genres = re.search(r'Genres:(.+)Voice',informations)
                        languages = re.search(r'Voice:(.+)',informations)
                        texto = soup.find("div", class_="psw-c-bg-card-1 psw-l-w-1/1 psw-l-w-1/1@tablet-s psw-l-w-7/12@tablet-l psw-l-w-2/3@laptop psw-l-w-2/3@desktop psw-l-w-2/3@max psw-p-6 psw-p-y-6").text.strip()#Pega toda a tabela com as informações das avaliações
                        total_avaliadores = re.search(r'from (\d+) ratings', texto).group(1) # pega o total de avaliadores    
                        total_estrelas = re.search(r'(\d+\.\d+) stars', texto).group(1) #pega o total de estrelas
                        stars = [] #cria uma lista com a porcentagem de avaliação de cada estrela na ordem crescente:1-5
                        stars.append(re.search(r'One star(\d+\%)',texto).group(1))#search on the text the pattern
                        #returns an dictionary with all the information needed    
                        print("Método 4", end = " ")
                        return{
                            'platform':platform,
                            'languages': languages,
                            'genres' : genres,
                            'realese_date':realese_date,
                            'publisher' : publisher,
                            'description' : description,
                            'title' : titulo, 
                            'estrelas' : total_estrelas, 
                            'total_avaliadores': total_avaliadores,
                            'stars' : stars
                            }
                    except:
                        try:
                            titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-7 psw-l-line-break-word").text.strip() #pega o título do jogo
                            description = soup.find("p",class_="psw-c-t-2 psw-p-x-7 psw-p-y-6 psw-p-x-6@below-tablet-s psw-m-sub-x-7 psw-m-auto@below-tablet-s psw-c-bg-card-1").text.strip()
                            informations = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip() #gets some information from the game (publisher, platform,realese date)
                            platform = re.search(r'Platform:(.+)Release',informations).group(1) #extracts the Platform
                            realese_date = re.search(r'Release:(\d+\/\d+\/\d+)Publisher',informations).group(1)
                            publisher = re.search(r'Publisher:(.+)Genres',informations).group(1)
                            genres = re.search(r'Genres:(.+)Voice',informations).group(1).split(',')
                            languages = re.search(r'Voice:(.+)',informations).group(1).split(',')
                            total_avaliadores = " "
                            total_estrelas = " "
                            stars = []        
                            #returns an dictionary with all the information needed    
                            print("Método 5", end = " ")
                            return{
                                'platform':platform,
                                'languages': languages,
                                'genres' : genres,
                                'realese_date':realese_date,
                                'publisher' : publisher,
                                'description' : description,
                                'title' : titulo, 
                                'estrelas' : total_estrelas, 
                                'total_avaliadores': total_avaliadores,
                                'stars' : stars
                                } 
                        except:
                            try:
                                titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-7 psw-l-line-break-word").text.strip() #pega o título do jogo
                                description = soup.find("p",class_="psw-c-t-2 psw-p-x-7 psw-p-y-6 psw-p-x-6@below-tablet-s psw-m-sub-x-7 psw-m-auto@below-tablet-s psw-c-bg-card-1").text.strip()
                                informations = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip() #gets some information from the game (publisher, platform,realese date)
                                platform = re.search(r'Platform:(.+)Release',informations).group(1) #extracts the Platform
                                realese_date = re.search(r'Release:(\d+\/\d+\/\d+)Publisher',informations).group(1)
                                publisher = re.search(r'Publisher:(.+)Genres',informations).group(1)
                                genres = re.search(r'Genres:(.+)Voice',informations)
                                languages = re.search(r'Voice:(.+)',informations)
                                total_avaliadores = " "
                                total_estrelas = " "
                                stars = [] 
                                #returns an dictionary with all the information needed    
                                print("Método 6", end = " ")
                                return{
                                    'platform':platform,
                                    'languages': languages,
                                    'genres' : genres,
                                    'realese_date':realese_date,
                                    'publisher' : publisher,
                                    'description' : description,
                                    'title' : titulo, 
                                    'estrelas' : total_estrelas, 
                                    'total_avaliadores': total_avaliadores,
                                    'stars' : stars
                                    } 
                            except:
                                try:
                                    titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-8 psw-l-line-break-word").text.strip() #pega o título do jogo
                                    description = soup.find("p",class_="psw-c-t-2 psw-p-x-7 psw-p-y-6 psw-p-x-6@below-tablet-s psw-m-sub-x-7 psw-m-auto@below-tablet-s psw-c-bg-card-1").text.strip()
                                    informations = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip() #gets some information from the game (publisher, platform,realese date)
                                    platform = re.search(r'Platform:(.+)Release',informations).group(1) #extracts the Platform
                                    realese_date = re.search(r'Release:(\d+\/\d+\/\d+)Publisher',informations).group(1)
                                    publisher = re.search(r'Publisher:(.+)Genres',informations).group(1)
                                    genres = re.search(r'Genres:(.+)Voice',informations)
                                    languages = re.search(r'Voice:(.+)',informations)
                                    total_avaliadores = " "
                                    total_estrelas = " "
                                    stars = [] 
                                    #returns an dictionary with all the information needed    
                                    print("Método 7", end = " ")
                                    return{
                                        'platform':platform,
                                        'languages': languages,
                                        'genres' : genres,
                                        'realese_date':realese_date,
                                        'publisher' : publisher,
                                        'description' : description,
                                        'title' : titulo, 
                                        'estrelas' : total_estrelas, 
                                        'total_avaliadores': total_avaliadores,
                                        'stars' : stars
                                        }
                                except:
                                       titulo = soup.find("h1", class_="psw-m-b-5 psw-t-title-l psw-t-size-6 psw-l-line-break-word").text.strip() #pega o título do jogo
                                       description = soup.find("p",class_="psw-c-t-2 psw-p-x-7 psw-p-y-6 psw-p-x-6@below-tablet-s psw-m-sub-x-7 psw-m-auto@below-tablet-s psw-c-bg-card-1").text.strip()
                                       informations = soup.find("dl", class_="psw-l-grid psw-fill-x psw-m-y-0").text.strip() #gets some information from the game (publisher, platform,realese date)
                                       platform = re.search(r'Platform:(.+)Release',informations).group(1) #extracts the Platform
                                       realese_date = re.search(r'Release:(\d+\/\d+\/\d+)Publisher',informations).group(1)
                                       publisher = re.search(r'Publisher:(.+)Genres',informations).group(1)
                                       genres = re.search(r'Genres:(.+)Voice',informations)
                                       languages = re.search(r'Voice:(.+)',informations)
                                       total_avaliadores = " "
                                       total_estrelas = " "
                                       stars = [] 
                                       #returns an dictionary with all the information needed    
                                       print("Método 8", end = " ")
                                       return{
                                           'platform':platform,
                                           'languages': languages,
                                           'genres' : genres,
                                           'realese_date':realese_date,
                                           'publisher' : publisher,
                                           'description' : description,
                                           'title' : titulo, 
                                           'estrelas' : total_estrelas, 
                                           'total_avaliadores': total_avaliadores,
                                           'stars' : stars
                                           }
def playstation():
    #Cria um dicionário para guardar todos os jogos
    games = {}
    k=1
    #Irá pegar todos os jogos de uma página em específico da playstation
    for i in range(1,10):
        url = f"https://store.playstation.com/en-us/pages/browse/{i}"    
        links = links_playstation(url)
        for link in links[1:]:
            try:
                print(f"{k} jogos capturados na Playstation")
                k+=1
                informacoes = informacoes_playstation(link)
                titulo = informacoes['title'] #a chave de meu dicionário será o título de um jogo
                games[titulo] = informacoes # o valor de um jogo será suas informações
            except Exception as error:
                print(f"Erro ao trabalhar sobre {link} : {error}")
                continue
    #os.system("cls")
    return games #retorna um dicionário que guarda as informações dos jogos 