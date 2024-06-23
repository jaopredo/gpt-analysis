'''
This module we'll collect games info that are on Steam 
'''

import requests
from bs4 import BeautifulSoup
import re
import time


def pesquisa_google(jogo):
    """
    Here we search a game on google and takes the valid Steam link
    """

    #https://www.bing.com/search?q=dead+by+daylight+steam
    jogo = re.sub(' ','+', jogo)   # replace the blank spaces for +
    url_google = f"https://www.google.com/search?q={jogo}steam"
    page = requests.get(url_google)
    soup = BeautifulSoup(page.text,"lxml")
    fatias = soup.find_all("div", class_="egMi0 kCrYT")

    for fatia in fatias:    
        try:
            link = fatia.find("a")
            link = link['href']
            id_jogo = re.search(r'/app/(\d+)', link).group(1)                    
            link = f"https://store.steampowered.com/app/{id_jogo}"
            #print(link)
            return [id_jogo,link]   # return the Steam game link to the code
        except:
            continue
   

def arrumar_data(data):
    """
    Here we fix the date format. It comes like this: Posted : date (with a comma and some without the year number) 
    """

    data = re.search(r'Posted: (.+)',data).group(1)  # take the date
    data = re.sub(',', '',data)   # cut the comma
    
    cont = 0
    for i in data:
        if i == ' ':
            cont+=1
    if cont == 1:
        data = data + " 2024"  # in case the year doesn't appear, we add '2024'
    
    dia = int(data[0:2])
    resto = data[2:].strip()  #  function 'resto' contains everything that isn't the day number
    ano = resto[-4:]
    dicio = {'January': '01',
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
    mes = resto[:-4].strip()
    mes = dicio[mes]
    data = f'{dia}/{mes}/{ano}'
    
    return data


def arrumar_opinioes(opinioes):
    """
    Function to fix and format the reviews. 
    """
    
    # each comment has up to 4 types: helpful-funny(1), helpful(2), funny(3) and, neither(4):

    if opinioes == 'N/I':  # case 4
        return ['0', '0'] 
    option = opinioes.split('\t')[0]
    #print('---------',opinioes)

    if 'helpful' and 'funny' in opinioes:  # case 1 
        try:
            opinioes = re.search(r'(.+) people found this review helpful(.+) people found this review funny',option)
            helpful = opinioes.group(1)
            funny = opinioes.group(2)
            return [helpful, funny]
        except:
            opinioes = re.search(r'(.+) people',option)
            helpful = opinioes.group(1)
            funny = 1
            return [helpful, funny]
            
    if 'helpful' in opinioes:  # case 2
        try: 
            opinioes = re.search(r'(.+) people found this review helpful',option)
            helpful = opinioes.group(1)
            return [helpful,'0']
        except:
            opinioes = re.search(r'(.+) person found this review helpful',option)
            helpful = opinioes.group(1)
            return [helpful,'0']

    if 'funny' in opinioes:  #case 3
        try:
            opinioes = re.search(r'(.+) people found this review funny',option)
            funny = opinioes.group(2)
            return ['0', funny]
        except:
            opinioes = re.search(r'(.+) person found this review funny',option)
            funny = opinioes.group(2)
            return ['0', funny]


def  coletar_dados(pessoa):
    """
    Here we collect info about a especific comment
    """
    
    # collecting:
    data = pessoa.find("div", class_="date_posted").text.strip()
    horas = pessoa.find("div", class_="hours").text.strip()  # it is on this format: '{horas} hrs on record'
    comentario = pessoa.find("div", class_="apphub_CardTextContent").text.strip() # take a large block of code that contains the date and the comment
    final_opinion = pessoa.find("div", class_="title").text.strip()
    try:
        opinioes = pessoa.find("div", class_="found_helpful").text.strip()
    except:
        opinioes = "N/I"
        
    # cleaning:
    data = arrumar_data(data)  # clean the date number
    horas = re.search(r'(.+) hrs on record',horas).group(1)  # clean the hour number
    comentario = re.search(r'Posted: (.+)\n(.+)',comentario).group(2).strip()  # take only the comment
    comentario = re.sub(';', '.', comentario)  # replace ';' for '.' to avoid formatting errors on Excel
    helpful,funny = arrumar_opinioes(opinioes)
    horas = re.sub(',','',str(horas))
    horas = re.sub(r'\.',',',horas)
    helpful = re.sub(',','', str(helpful))
    funny = re.sub(',','',str(funny))
    if final_opinion == 'Recommended':
        final_opinion = 1
    else:
        final_opinion = 0
    
    
    return [comentario, final_opinion, horas, data, helpful, funny]  # return a list in the specified order we want
    

def coletar_comentarios(link_main, id_jogo):
    """
    Here we collect the comments infos about a game
    """
    
    link_comentarios = f"https://steamcommunity.com/app/{id_jogo}/reviews/?browsefilter=toprated&snr=1_5_100010_"  # the link
    page = requests.get(link_comentarios)
    soup = BeautifulSoup(page.text, "lxml")
    comentarios = soup.find_all("div",  class_="apphub_UserReviewCardContent")  # take all the comments and create a list
    dados_comentarios = []  # list that will keep all the collected comments

    for pessoa in comentarios:  # for each comment, collect and clean
        dados_comentario = coletar_dados(pessoa)  # collect the data on a list
        dados_comentarios.append(dados_comentario)
    
    return dados_comentarios


def coletar_preco(tabela_valores):
    """
    Here we'll collect the price of a specific game, caring about the discount and the whole price
    """

    try:  # desconsidering the discount:
        temp = []
        precos = tabela_valores.find_all("div", class_="game_purchase_price price")
        for preco_jogo in precos:
            print(preco_jogo.text.strip())
            if 'Free' in preco_jogo.text.strip():
                return '00,00'
            if 'DEMO' in preco_jogo.text.strip():
                continue
            if '$' not in preco_jogo.text.strip():
                continue
            temp.append(preco_jogo)
            if len(temp) != 0:
                return preco_jogo.text.strip()[2:]
            a = preco_jogo.group(1)
            print("!"*50)
        precos.group('1')
    except:
        try:  # considering that the game has the discount:
            frase = tabela_valores.find("div", class_="discount_block game_purchase_discount").text  # take a phrase with the discount and the final price
            desconto = tabela_valores.find("div", class_="discount_pct").text.strip()[1:]
            preco_original = tabela_valores.find("div", class_="discount_original_price").text.strip()
            preco_final = tabela_valores.find("div", class_="discount_final_price").text.strip()
            
            return preco_final[3:]
        except:
            try:  # considering that there is a discount on the price for buying DLCs:
                preco_final = tabela_valores.find("div", class_="discount_final_price").text[2:]
                preco_final = re.sub(',','.',preco_final)  # take out the commas
                preco_final = re.sub(' ','',preco_final)  # take out the blank spaces
                desconto = tabela_valores.find("div", class_="bundle_base_discount").text.strip()[1:-1]
                desconto = re.sub(' ', '',desconto)  # take out blank spaces, again
                desconto = float(desconto)/100
                preco_final = float(preco_final)
                preco_original = preco_final/(1-desconto)

                return(preco_original[2:])
            except:
                try:
                    preco = tabela_valores.find("div", class_="discount_final_price").text.strip()
                    print(preco)
                    return preco[2:]
                except:    
                    return "00,00"
        
   
def coletar_genero(soup):
    """
    Here we collect the game category
    """

    try:
        tabela = soup.find("div", class_="details_block")  # take some infos
        genero = re.search(r'Genre:(.+)\n',tabela.text).group(1).strip() # take the game category
        genero = genero.split(',')[0] #cleaning and only extracting the first genre of the list
        return genero
    except:
        try:
            tabela = soup.find("div", class_="block_content_inner")
            genero = re.search(r'Genre:(.+)\n',tabela.text).group(1).strip()
            genero = genero.split(',')[0]
            return genero
        except:
            print("genero")
            
                
def coletar_informacoes_do_jogo(jogo):
    """
    Here we collect the infos about a game
    """
    
    id_jogo,link_main = pesquisa_google(jogo)  # take the game's home page link on Steam and his id
    page = requests.get(link_main)
    print(jogo.strip(),'---',link_main)
    soup = BeautifulSoup(page.text,"lxml")
    genero = coletar_genero(soup)
    dados_comentarios = coletar_comentarios(link_main,id_jogo)  # collect the comments about the game
    tabela_valores = soup.find("div", class_="game_area_purchase")
    preco_jogo = coletar_preco(tabela_valores)
    return [genero, dados_comentarios,preco_jogo]


def steam():
    with open('data/steam_games.csv', 'w', encoding = 'utf-8') as arquivo:
        arquivo.write('GAME ID;CATEGORY;PRICE;COMMENT;FINAL OPINION;HOURS SPENT;DATE OF THE COMMENT; HELPFUL; FUNNY;\n')
    
    with open('data/steam_companies.csv','w', encoding='utf-8') as file:
        file.write('COMPANY ID; COMPANY\n') 
    
    with open('data/steam_game_company.csv','w',encoding = 'utf-8') as file:
        file.write('GAME ID;GAME NAME;GAME COMPANY ID\n')
    
    with open('data/steam_list.csv','r',encoding = 'utf-8') as arquivo:
        game_id = -1
        for company_id,linha in enumerate(arquivo):  # each line is in this format : 'Epic Games||||Fortnite||||Gears of War||||Infinity Blade||||Fortnite Chapter 2 Season 8||||Tony Hawk's Pro Skater 1+2'

            lista = linha.split('||||')
            empresa = lista[0].strip()
            print('\n\n',empresa)
            
            for jogo in (lista[1:]):
                game_id += 1
                
                #writing on the steam_game_company.csv, so we can search fo an game end its company:
                with open('data/steam_game_company.csv', 'a', encoding = 'utf-8') as file:
                    file.write(f'{game_id};{jogo.strip()};{company_id}\n')
                
                try:
                    genero, dados_comentarios, preco_jogo = coletar_informacoes_do_jogo(jogo)
                    escrever(game_id,jogo.strip(),genero,preco_jogo,dados_comentarios)
                except Exception as error:
                    print('#############',error)
                    
            with open('data/steam_companies.csv','a',encoding = 'utf-8') as file:
                file.write(f'{company_id};{empresa}\n')


def escrever(game_id,jogo,genero,preco_jogo,dados_comentarios):
    
    with open('data/steam_games.csv', 'a', encoding = 'utf-8' ) as arquivo:
        for info in dados_comentarios:
            # comment, final opinion, hours, date, helpful, funny
            arquivo.write(f'{game_id};{genero};{preco_jogo};{info[0]};{info[1]};{info[2]};{info[3]};{info[4]};{info[5]}\n')



