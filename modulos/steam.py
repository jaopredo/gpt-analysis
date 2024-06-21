import requests
from bs4 import BeautifulSoup
import re
import time


def pesquisa_google(jogo):
    """
    Pesquisa um jogo no google e pega o link da steam válido
    """
    #https://www.bing.com/search?q=dead+by+daylight+steam
    jogo = re.sub(' ','+', jogo) #substitui os espaços em branco por +
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
            return [id_jogo,link]    #retorna o link do jogo na Steam para o programa
        except:
            continue
   
def arrumar_data(data):
    """
    Aqui se arruma a fromatação da data, pois ela entra assim: Posted : data(com vírgula e alguns sem o ano)
    """
    data = re.search(r'Posted: (.+)',data).group(1) #pega a data
    data = re.sub(',', '',data) #Retira-se a vírgula
    
    cont = 0
    for i in data:
        if i == ' ':
            cont+=1
    if cont == 1:
        data = data + " 2024" #caso não contenha o ano, adiociona-se o ano de 2024.
    
    dia = int(data[0:2])
    resto = data[2:].strip() # o resto contém tudo que não é o dia
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
    Aqui se arruma e formata as opiniões. 
    """
    
    #Cada comentário pode ser de até 4 tipos: helpful-funny(1), helpful(2), funny(3) e, ainda, nenhum dos dois(4):
    if opinioes == 'N/I': #caso 4
        return ['N/I', 'N/I']
    
    option = opinioes.split('\t')[0]
    #print('---------',opinioes)
    if 'helpful' and 'funny' in opinioes: #caso 
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
            
    if 'helpful' in opinioes: #caso 2
        try: 
            opinioes = re.search(r'(.+) people found this review helpful',option)
            helpful = opinioes.group(1)
            return [helpful,'N/I']
        except:
            opinioes = re.search(r'(.+) person found this review helpful',option)
            helpful = opinioes.group(1)
            return [helpful,'N/I']
    if 'funny' in opinioes: #caso 3
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
    Aqui se oletam as informções de um comentário em específico
    """
    
    #coletando:
    data = pessoa.find("div", class_="date_posted").text.strip()
    horas = pessoa.find("div", class_="hours").text.strip() #está na forma {horas} hrs on record
    comentario = pessoa.find("div", class_="apphub_CardTextContent").text.strip() #pega um gande bloco de texto que contém a data e o comentário em si
    opiniao_final = pessoa.find("div", class_="title").text.strip()
    try:
        opinioes = pessoa.find("div", class_="found_helpful").text.strip()
    except:
        opinioes = "N/I"
        
    #limpando:
    data = arrumar_data(data) #limpo a data
    horas = re.search(r'(.+) hrs on record',horas).group(1) #limpo a hora
    comentario = re.search(r'Posted: (.+)\n(.+)',comentario).group(2).strip() #pega somente o comentario
    comentario = re.sub(';', '.', comentario) # subistitui os ; por . para evitar erros de formatação no excel
    helpful,funny = arrumar_opinioes(opinioes)
    return [comentario, opiniao_final, horas, data, helpful, funny] #retorna uma lista na ordem especificada ali
    
def coletar_comentarios(link_main,id_jogo):
    """
    Aqui se coletam as informações dos comentários em um jogo
    """
    
    link_comentarios = f"https://steamcommunity.com/app/{id_jogo}/reviews/?browsefilter=toprated&snr=1_5_100010_" # o link do site
    page = requests.get(link_comentarios)
    #print(link_main)
    soup = BeautifulSoup(page.text, "lxml")
    comentarios = soup.find_all("div",  class_="apphub_UserReviewCardContent") #pega todos os comentários e cria uma lista
    dados_comentarios = [] # lista onde seram guardados todos os comentários coletados do jogo 
    for pessoa in comentarios: #para cada comentário faz a coleta e limpagem
        dados_comentario = coletar_dados(pessoa) #coleta os dados em uma lista
        dados_comentarios.append(dados_comentario)
    
    return dados_comentarios

def coletar_preco(tabela_valores):
    """
    Aqui se busca coletar o preço de um jogo em específico, cuidando dos parâmentros desconto e valor cheio
    """
    try: #desconsiderando o desconto:
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
                return preco_jogo.text.strip()
    except:
        try: #considerando que o jogo esteja com desconto e possa ser vendido separadamente:
            frase = tabela_valores.find("div", class_="discount_block game_purchase_discount").text # pega uma frase com valores de desconto e preço final
            desconto = tabela_valores.find("div", class_="discount_pct").text.strip()[1:]
            preco_original = tabela_valores.find("div", class_="discount_original_price").text.strip()
            preco_final = tabela_valores.find("div", class_="discount_final_price").text.strip()
            
            return preco_final
        except:
            try: #considerando que haja desconto no preço por compra de pacotes:
                preco_final = tabela_valores.find("div", class_="discount_final_price").text[3:]
                preco_final = re.sub(',','.',preco_final) #retira as virgulas
                preco_final = re.sub(' ','',preco_final) #retira os espaçoes em branco
                desconto = tabela_valores.find("div", class_="bundle_base_discount").text.strip()[1:-1]
                desconto = re.sub(' ', '',desconto) #retira espaço em branco
                desconto = float(desconto)/100
                preco_final = float(preco_final)
                preco_original = preco_final/(1-desconto)

                return(preco_original)
                
            except:
                print("preço")
        

    
def coletar_genero(soup):
    """
    Aqui se coleta o gênero do jogo
    """
    try:
        tabela = soup.find("div", class_="details_block") # pega algumas informacoes
        genero = re.search(r'Genre:(.+)\n',tabela.text).group(1).strip() # pega o genero do jogo
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
    Aqui se coletam as informações de um jogo
    """
    
    id_jogo,link_main = pesquisa_google(jogo) # pega o link da pagina principal do jogo na steam e também o id dele 
    page = requests.get(link_main)
    print(jogo,'---',link_main)
    soup = BeautifulSoup(page.text,"lxml")
    genero = coletar_genero(soup)
    dados_comentarios = coletar_comentarios(link_main,id_jogo)    #coleta os comentarios daquele jogo
    #preco_jogo = soup.find("div", class_="game_purchase_price price").text.strip() #coleta o preço do jogo
    tabela_valores = soup.find("div", class_="game_area_purchase")
    preco_jogo = coletar_preco(tabela_valores)
    return [genero, dados_comentarios,preco_jogo]

def steam():
    with open('dados/steam_list.csv','r',encoding = 'utf-8') as arquivo:
        for linha in arquivo: #cada linha está nessa forma : Epic Games||||Fortnite||||Gears of War||||Infinity Blade||||Fortnite Chapter 2 Season 8||||Tony Hawk's Pro Skater 1+2
            lista = linha.split('||||')
            empresa = lista[0].strip()
            print('\n\n',empresa)
            for jogo in lista[1:]:
               # print(jogo.strip())
                try:
                    genero, dados_comentarios, preco_jogo = coletar_informacoes_do_jogo(jogo)
                    escrever(empresa,jogo.strip(),genero,preco_jogo,dados_comentarios)
                except Exception as error:
                    print('#############',error)

def escrever(empresa,jogo,genero,preco_jogo,dados_comentarios):
    with open('dados/steam.csv', 'a', encoding = 'utf-8' ) as arquivo:
        for info in dados_comentarios:
            #comentario, opiniao_final, horas, data, helpful, funny
            arquivo.write(f'{empresa};{jogo};{genero};{preco_jogo};{info[0]};{info[1]};{info[2]};{info[3]};{info[4]};{info[5]}\n')

with open('dados/steam.csv', 'w', encoding = 'utf-8') as arquivo:
    arquivo.write('EMPRESA;JOGO;GÊNERO;PREÇO;COMENTARIO;OPINIAO FINAL; HORAS DE JOGO DO USUÁRIO; DATA DE PUBLICAÇÃO DO COMENTÁRIO; HELPFUL; FUNNY;\n')

    
steam()
#coletar_informacoes_do_jogo("Prey")
#coletar_informacoes_do_jogo("Grand Theft Auto: The Trilogy - The Definitive Edition")
    
    
    