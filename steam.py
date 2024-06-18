from bs4 import BeautifulSoup
import requests
import re

def links_steam(url):
    """
    Pega o endereço de uma pesquisa na steam e coleta todos os links de jogos disponíveis nela (aproximadamente 50 por página)
    """
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    result = soup.find_all("a", class_="search_result_row") #acha todos os termos que possuem a categoria de ednereço de link
    links_main = []
    for pedaco in result:
        links_main.append(pedaco.get('href')) #para cada parte de result, ele irá achar o valor correspondente do jogo 
    return(links_main)   #Irá retornar uma lista com todas as páginas dos jogos encontrados na primeira principal da pesquisa

def preco_steam(link_main):
    """
    Coleta o preço de um jogo em específico apartir de sua página
    """
    #deverá pegar os links diponibilizados por links_steam()
    page = requests.get(link_main)
    soup = BeautifulSoup(page.text, "lxml")
    preco = soup.find("div", class_="game_purchase_price price")#pega o primeiro preco disponível na steam    
    if preco:
        return preco.text.strip()    #tenta achar o preço disponível
    return "NOT FOUNDED" #caso não ache, irá retornar esta resposta

def comentarios_steam(link_comentarios):
    """
    Irá, apartir de uma página de um jogo específico, coletar as informações dos comentários
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'} #Como serão feitas muitas requisições, é interessante passar um User-Agent, assim evitando ser bloqueado pelo site
    page = requests.get(link_comentarios, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    tabela = soup.find_all("div", class_="apphub_Card modalContentLink interactable") #pega todos os espaços de comentários
    informacoes = []
    for categoria in tabela:
        informacoes.append(categoria.text.strip()) # pega as tabelas de cada comentário e começa a limpá-los:
    comments = {} #este dicionário servirá para guardar as informações dos comentários dos usuários no jogo em específico
    for info in informacoes:  #Agora começa a limpar os dados
        cleaned = re.sub(r'[\n\t\r]',' ',info) #retira todas as quebras de linhas e tabulações
        lista = cleaned.split('  ')#separa em forma de lista, onde o delimitador são dois espaços em branco
        nova = [] #cria uma lista que irá armazenar as informações(opinião do povo, nome do jogador, )
        for i in lista:
            if i.strip():
                nova.append(i)  #coloca as informações na lista acima descrita
        #agora vai pegando conforme se é necessário:
    #-----------------------parte de coleta de dados---------------#
        general_opinion = nova[0] 
        final_opinion_of_the_user = nova[2]
        posted=nova[3][8:20]
        if(len(nova[3].strip())<12):
            posted = nova[3][1:12]
        else:
            temp = re.search('(\d+) (.+), (\d+)',nova[3])
            if temp:
                posted = temp.group(1) + " " +temp.group(2) +", "+temp.group(3)
        commentary = re.sub(';', '.', nova[4])
        user = nova[5].split(' ')[1]
        user_games = "NOT INFORMED"
        if(len(nova[5].split(' ')) >=3):
            user_games = nova[5].split(' ')[2:]
            if(len(user_games) == 4):
                user_games = ' '.join(user_games)
            else:
                user_games = "NOT INFORMED"                
        #------------------------------------------------------------#
        #a chave será o nome do usuário e o valor as informaçõe que este forneceu no comentário
        comments[user] = {
                'user_name' : user,
                'user_games':user_games,
                'general_opinion_of_people' : general_opinion,
                'final_opinion' : final_opinion_of_the_user,
                'commentary': commentary,
                'date': posted}
    
    
    return comments #retorna um dicionário com as informações dos comentários de um jogo específico

def title_steam(link_main):
    """
    Irá colher o título do jogo em sua página
    """
    page = requests.get(link_main)
    soup = BeautifulSoup(page.text,"lxml")
    title = soup.find("div", class_="apphub_AppName").text.strip()
    return(title)

def change_link_steam(link_main):
    """
    Serve para colher o ID de um número e escrever o seu endereço na Steam
    """
    magic_number = link_main.split('/')[4] # Cada jogo possui um ID, apenas extraio ele 
    link_comentarios = "https://steamcommunity.com/app/" + f"{magic_number}" + "/?browsefilter=toprated&snr=1_5_100010_" #Todos terão esta forma, entãoo basta subistituirmos
    return link_comentarios #Retorna o link do jogo

def criar_links_steam():
    """
    Aqui, cria-se links de pesquisa, onde cada página conterá até 50 jogos. Útil quando se deseja procurar um jogo em específico
    """
    links = [] #Cria a lista que conterá os links
    lista = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','t','s','t','u','v','w','x','y','z'] #cada elemento nesta lista será uma pesquisa 
    for pesquisa in lista:
        links.append(f"https://store.steampowered.com/search/?term={pesquisa}&supportedlang=brazilian&filter=topsellers&ndl=1")
    return links #retorna a lisa com os links de pesquisa gerados

def steam():
    """
    Esta é a principal função do módulo, pois ela serve como o gerente do projeto de extração, manda os funcionários (as outras funções) fazerem o seu trabalho
    """
    k=1 #Serve para mostrar em qual link de pesquisa estamos no momento
    i=1 #Serve para mostrar quantos jogos já foram pegos no total
    links = criar_links_steam() # pega os links de pesquisa
    games_list = [] #cria uma lista que conterá as informações de cada jogo
    for url in links:  #para cada pesquisa irá realizar as tarefas acima mencionado  
        games = {}
        print("-----------------------------------")
        print(f"Buscando no link {k}")
        links_main = links_steam(url)
        j=0 #servirá para delimitar quantos jogos ao máximo iremos extrair de cada página de pesquisa
        for link_main in links_main:
            try: #Caso haja alguma falha, o programa irá nos sinalizar e pular o link em específico
                j+=1
                print(f"Capturou {i} jogos na Steam" )
                title = title_steam(link_main) #pega o título
                price = preco_steam(link_main) #pega o preço
                commentary = comentarios_steam(change_link_steam(link_main))#pega os comentários
                games[title]={'title' : title,
                              'price' : price,
                              'commentary' : commentary} #adiciona no dicionário a chave (título do jogo) e o valor (informações do jogo)
                i+=1
                if(j >= 50):
                    games_list.append(games) #adiciona o dicionário dos jogos à lista de jogos
                    break
            except Exception as error: #caso haja erro:
                print(f"Erro no link {link_main} : {error}") #mostra o erro gerado
                continue
        k+=1
    return games_list # retorna a lista contento as informações de todos os jogos
    
steam()