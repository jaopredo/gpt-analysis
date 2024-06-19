import requests
from bs4 import BeautifulSoup
import re

def pegar_lista_empresas():
    lista = []
    with open('lista_de_pesquisa.csv', 'r', encoding='utf-8') as arquivo:
        for li in arquivo:
            lista.append(li)
        return li

def achar_url(jogo):
    jogo = re.sub(' ', '+',jogo) + "+game+imdb"
    link = f"https://www.google.com.br/search?q={jogo}"
    page = requests.get(link)
    soup = BeautifulSoup(page.text,"lxml")
    fatia = soup.find("div", class_="egMi0 kCrYT")
    link = fatia.find("a")
    link = link['href']
    link = re.search(r'/url\?q=(.+?)&sa=',link).group(1)
    return(link+"reviews/?ref_=tt_ov_rt")    
    
achar_url("the last of us")

def info_pessoa(pessoa):
    """
    Pega o comentário de uma pessoa e extrai os dados dele
    """
    lista_pessoal=[]
    titulo = re.sub(';','.', pessoa.find("a", class_="title").text.strip())
    comentario = re.sub(';','.',pessoa.find("div", class_="text show-more__control").text.strip())
    comentario = re.sub(r'\s+', ' ', comentario)
    comentario = re.sub(r'\n', ' ',comentario)
    #print(titulo)
    try:
        nota = pessoa.find("span", class_="rating-other-user-rating").text.strip()
    except:
        nota = "Not Informed"
    data = pessoa.find("span", class_="review-date").text.strip()
    opiniao_pessoas = pessoa.find("div", class_="actions text-muted").text.strip().split('  ')[0]
    lista_pessoal.append(titulo)
    lista_pessoal.append(comentario)
    lista_pessoal.append(nota)
    lista_pessoal.append(data)
    lista_pessoal.append(opiniao_pessoas)
    return lista_pessoal

def buscar_informacoes_do_jogo(jogo):
    link = achar_url(jogo)
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    
    info_pessoas = soup.find_all("div", class_="lister-item mode-detail imdb-user-review collapsable")
    lista_jogo = [] #contém os comentários de um certo jogo
    contagem = 1
    #Para cada comentário irá se extrair os dados:
    for pessoa in info_pessoas:
        if(contagem>20):
            break
        #Aqui se extrai tudo que é necessário do comentário
        lista_pessoal= info_pessoa(pessoa) #contém informações, nesta ordem:[titulo,comentario,nota,data,opiniao_pessoas]
        lista_jogo.append(lista_pessoal)
        contagem+=1    
        
    return lista_jogo

def escrever(lista_comentarios_empresa):
    with open('dados/imdb.csv', 'a', encoding = 'utf-8') as arquivo:
        empresa = lista_comentarios_empresa[0]
        for game in lista_comentarios_empresa[1:]:
            jogo = game[0]
            lista = game[1]
            for pessoa in lista:
                arquivo.write(f"{empresa};{jogo};{pessoa[0]};{pessoa[1]};{pessoa[2]};{pessoa[3]};{pessoa[4]}")
def buscar_jogos_da_empresa(info):
    #info está neste formato:Empresa1||||jogo_grande_1||||jogo_grande_2||||jogo_grande_3||||jogo_recente_1||||jogo_recente_2
    info = info.split('||||')
    empresa = info[0]
    jogos = info[1:]
    lista_comentarios_empresa = [empresa]
    for jogo in jogos:
        lista_comentarios_empresa.append([jogo,buscar_informacoes_do_jogo(jogo)])
    escrever(lista_comentarios_empresa)
    
with open('dados/imdb.csv', 'w',encoding='utf-8') as arquivo:
    arquivo.write("EMPRESA;JOGO;TITULO DO COMENTÁRIO;COMENTÁRIO;NOTA;DATA;OPINIÃO DAS PESSOAS SOBRE O COMENTÁRIO"+"\n")

#buscar_jogos_da_empresa("Nintendo||||The Legend of Zelda: Breath of the Wild||||Super Mario Odyssey||||Animal Crossing: New Horizons||||The Legend of Zelda: Tears of the Kingdom||||Metroid Dread")


with open('dados/lista_de_pesquisa.csv','r',encoding = 'utf-8') as arquivo:
    i=1
    for info in arquivo:
        #print(info)
        
        buscar_jogos_da_empresa(info.strip())
        i+=1
