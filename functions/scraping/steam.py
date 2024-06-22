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
        return ['N/I', 'N/I'] 
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
            return [helpful,'N/I']
        except:
            opinioes = re.search(r'(.+) person found this review helpful',option)
            helpful = opinioes.group(1)
            return [helpful,'N/I']

    if 'funny' in opinioes:  #case 3
        try:
            opinioes = re.search(r'(.+) people found this review funny',option)
            funny = opinioes.group(2)
            return ['N/I', funny]
        except:
            opinioes = re.search(r'(.+) person found this review funny',option)
            funny = opinioes.group(2)
            return ['N/I', funny]


def  coletar_dados(pessoa):
    """
    Here we collect info about a especific comment
    """
    
    # collecting:
    data = pessoa.find("div", class_="date_posted").text.strip()
    horas = pessoa.find("div", class_="hours").text.strip()  # it is on this format: '{horas} hrs on record'
    comentario = pessoa.find("div", class_="apphub_CardTextContent").text.strip() # take a large block of code that contains the date and the comment
    opiniao_final = pessoa.find("div", class_="title").text.strip()
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
    horas = re.sub(',','',horas)
    helpful = re.sub(',','', helpful)
    funny = re.sub(',','',funny)
    return [comentario, opiniao_final, horas, data, helpful, funny]  # return a list in the specified order we want
    

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
        precos = tabela_valores.find_all("div", class_="game_purchase_price price")
        for preco_jogo in precos:
            print(preco_jogo.text.strip())
            if 'Free' in preco_jogo.text.strip():
                return 'R$ 00,00'
            if 'DEMO' in preco_jogo.text.strip():
                continue
            if '$' not in preco_jogo.text.strip():
                continue
            if preco_jogo != None:
                return preco_jogo.text.strip()[2:]
    except:
        try:  # considering that the game has the discount:
            frase = tabela_valores.find("div", class_="discount_block game_purchase_discount").text  # take a phrase with the discount and the final price
            desconto = tabela_valores.find("div", class_="discount_pct").text.strip()[1:]
            preco_original = tabela_valores.find("div", class_="discount_original_price").text.strip()
            preco_final = tabela_valores.find("div", class_="discount_final_price").text.strip()
            
            return preco_final[2:]
        except:
            try:  # considering that there is a discount on the price for buying DLCs:
                preco_final = tabela_valores.find("div", class_="discount_final_price").text[3:]
                preco_final = re.sub(',','.',preco_final)  # take out the commas
                preco_final = re.sub(' ','',preco_final)  # take out the blank spaces
                desconto = tabela_valores.find("div", class_="bundle_base_discount").text.strip()[1:-1]
                desconto = re.sub(' ', '',desconto)  # take out blank spaces, again
                desconto = float(desconto)/100
                preco_final = float(preco_final)
                preco_original = preco_final/(1-desconto)

                return(preco_original[2:])
            except:
                print("preço")
        
   
def coletar_genero(soup):
    """
    Here we collect the game category
    """

    try:
        tabela = soup.find("div", class_="details_block")  # take some infos
        genero = re.search(r'Genre:(.+)\n',tabela.text).group(1).strip() # take the game category
        return genero
    except:
        try:
            tabela = soup.find("div", class_="block_content_inner")
            genero = re.search(r'Genre:(.+)\n',tabela.text).group(1).strip()
            return genero
        except:
            print("genero")
            
                
def coletar_informacoes_do_jogo(jogo):
    """
    Here we collect the infos about a game
    """
    
    id_jogo,link_main = pesquisa_google(jogo)  # take the game's home page link on Steam and his id
    page = requests.get(link_main)
    print(jogo,'---',link_main)
    soup = BeautifulSoup(page.text,"lxml")
    genero = coletar_genero(soup)
    dados_comentarios = coletar_comentarios(link_main,id_jogo)  # collect the comments about the game
    tabela_valores = soup.find("div", class_="game_area_purchase")
    preco_jogo = coletar_preco(tabela_valores)
    return [genero, dados_comentarios,preco_jogo]


def steam():
    with open('data/steam.csv', 'w', encoding = 'utf-8') as arquivo:
        arquivo.write('GAME STUDIO;GAME NAME;CATEGORY;PRICE;COMMENT;FINAL OPINION;HOURS SPENT;DATE OF THE COMMENT; HELPFUL; FUNNY;\n')

    with open('data/steam_list.csv','r',encoding = 'utf-8') as arquivo:
        for linha in arquivo:  # each line is in this format : 'Epic Games||||Fortnite||||Gears of War||||Infinity Blade||||Fortnite Chapter 2 Season 8||||Tony Hawk's Pro Skater 1+2'
            lista = linha.split('||||')
            empresa = lista[0].strip()
            print('\n\n',empresa)
            for jogo in lista[1:]:
                try:
                    genero, dados_comentarios, preco_jogo = coletar_informacoes_do_jogo(jogo)
                    escrever(empresa,jogo.strip(),genero,preco_jogo,dados_comentarios)
                except Exception as error:
                    print('#############',error)


def escrever(empresa,jogo,genero,preco_jogo,dados_comentarios):
    with open('data/steam.csv', 'a', encoding = 'utf-8' ) as arquivo:
        for info in dados_comentarios:
            # comment, final opinion, hours, date, helpful, funny
            arquivo.write(f'{empresa};{jogo};{genero};{preco_jogo};{info[0]};{info[1]};{info[2]};{info[3]};{info[4]};{info[5]}\n')
