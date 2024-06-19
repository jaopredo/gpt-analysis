import requests
from bs4 import BeautifulSoup
import re

def pegar_lista_empresas():
    lista = []
    with open('lista_de_pesquisa.csv', 'r', encoding='utf-8') as arquivo:
        for li in arquivo:
            lista.append(li.strip())  # Adicionado strip() para remover espaços em branco
    return lista

def achar_url(jogo):
    jogo = re.sub(' ', '+',jogo) + "+game+imdb"
    link = f"https://www.google.com.br/search?q={jogo}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "lxml")
    fatia = soup.find("div", class_="egMi0 kCrYT")
    if fatia is None:
        return None
    link = fatia.find("a")
    if link is None:
        return None
    link = link['href']
    link = re.search(r'/url\?q=(.+?)&sa=', link)
    if link is None:
        return None
    return link.group(1) + "reviews/?ref_=tt_ov_rt"

def info_pessoa(pessoa):
    """
    Pega o comentário de uma pessoa e extrai os dados dele
    """
    lista_pessoal=[]
    titulo = pessoa.find("a", class_="title").text.strip()
    comentario = re.sub(';','.',pessoa.find("div", class_="text show-more__control").text.strip())
    nota = pessoa.find("span", class_="rating-other-user-rating")
    nota = nota.text.strip() if nota else "N/A"
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
    if not link:
        return []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "lxml")
    
    info_pessoas = soup.find_all("div", class_="lister-item mode-detail imdb-user-review collapsable")
    lista_jogo = [] #contém os comentários de um certo jogo
    contagem = 1
    #Para cada comentário irá se extrair os dados:
    for pessoa in info_pessoas:
        if contagem > 8:
            break
        #Aqui se extrai tudo que é necessário do comentário
        lista_pessoal = info_pessoa(pessoa) #contém informações, nesta ordem:[titulo,comentario,nota,data,opiniao_pessoas]
        lista_jogo.append(lista_pessoal)
        contagem += 1
    
    return lista_jogo

def escrever(lista_comentarios_empresa):
    with open('dados/imdb.csv', 'a', encoding='utf-8') as arquivo:
        empresa = lista_comentarios_empresa[0]
        print(lista_comentarios_empresa)
        for game in lista_comentarios_empresa[1:]:
            jogo = game[0]
            lista = game[1]
            #print(game)
            for pessoa in lista:
                if len(pessoa) == 5:  # Verifica se a lista tem 5 elementos
                    print(pessoa[0])
                    arquivo.write(f"{empresa};{jogo};{pessoa[0]};{pessoa[1]};{pessoa[2]};{pessoa[3]};{pessoa[4]}\n")
            print(f"passou {jogo}")

def buscar_jogos_da_empresa(info):
    #info está neste formato: Empresa1||||jogo_grande_1||||jogo_grande_2||||jogo_grande_3||||jogo_recente_1||||jogo_recente_2
    info = info.split('||||')
    empresa = info[0]
    jogos = info[1:]
    lista_comentarios_empresa = [empresa]
    for jogo in jogos:
        lista_comentarios_empresa.append([jogo, buscar_informacoes_do_jogo(jogo)])
    print(len(lista_comentarios_empresa))        
    escrever(lista_comentarios_empresa)

# Inicializa o arquivo com o cabeçalho
with open('dados/imdb.csv', 'w', encoding='utf-8') as arquivo:
    arquivo.write("EMPRESA;JOGO;TITULO DO COMENTÁRIO;COMENTÁRIO;NOTA;DATA;OPINIÃO DAS PESSOAS SOBRE O COMENTÁRIO\n")

# Buscar jogos da empresa Sony como exemplo
buscar_jogos_da_empresa("Sony Interactive Entertainment||||The Last of Us Part II||||Ghost of Tsushima||||God of War||||Ratchet & Clank: Rift Apart||||Returnal")

# Para buscar informações de empresas listadas no arquivo
lista_empresas = pegar_lista_empresas()
for info in lista_empresas:
    buscar_jogos_da_empresa(info)
