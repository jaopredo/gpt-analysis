import requests
from bs4 import BeautifulSoup
import time
import grapho
def coletar_amigos_da_pessoa(link_perfil_amigos):
    """
    Acessa o site com os amigos de uma pessoa e coleta todos os amigos dela
    Retorna uma lista com os perfis e tambémo endereço deste perfis
    """
    page = requests.get(link_perfil_amigos)
    soup = BeautifulSoup(page.text, "lxml")
    lista_amigos = soup.find_all("div", class_="friend_block_content")
    lista_links_amigos = soup.find_all("a", class_="selectable_overlay")
    amigos=[]
    links_perfil_amigos=[]
    for friend_link in lista_links_amigos:
        links_perfil_amigos.append(friend_link['href'])        
        
    for friend in lista_amigos:
        texto = ''.join(friend.find_all(string=True, recursive=False)).strip()
        amigos.append(texto)

    profiles= set()
    for i in range(len(amigos)):
        profiles.add(f"{amigos[i]}|||||{links_perfil_amigos[i]}/friends")
        
    return [profiles,amigos] #guarda uma lista com elementos neste formato: "{perfil_amigo}|||||{link_amigos_do_amigo}"

def adicionar_pessoas_no_dicionario(pessoas, amigos):
    
    for amigo in amigos:
        try:
            if amigo.split("|||||")[0] not in pessoas:
               pessoas[amigo.split('|||||')[0]] = amigo.split('|||||')[1]
        except:
            continue
    return pessoas

def adicionar_nomes_no_dicionario(usuarios, lista_nomes):
    for amigo in lista_nomes:
        usuarios.add(amigo.split('|||||')[0])
    return usuarios

def buscar(perfil,link_perfil,contador,num_max,ligacoes,perfis_varridos,set_username_link):
    if(contador >= num_max or perfil in perfis_varridos):
        return [ligacoes,contador,perfis_varridos,set_username_link]
    print(contador)
    perfis_varridos.add(perfil)    
    all_=coletar_amigos_da_pessoa(link_perfil)
    ligacoes[perfil] = all_[1]
    contador+=len(all_[1])
    set_username_link.update(all_[0])
    for individuo in all_[0]:
        try:
            perfil = individuo.split('|||||')[0]
            link_perfil = individuo.split('|||||')[1]
            if perfil not in perfis_varridos:
                lista = buscar(perfil,link_perfil,contador,num_max,ligacoes,perfis_varridos,set_username_link)
                ligacoes.update(lista[0])
                contador = lista[1]
                perfis_varridos = perfis_varridos.union(lista[2])
                set_username_link=lista[3]
                #print(set_username_link)
                #time.sleep(10)
                if contador >= num_max:
                   break
        except:
            continue
    return [ligacoes,contador,perfis_varridos,set_username_link]

def arvore_de_conxoes(perfis_varridos, url_0,_username_link):
    amigos = coletar_amigos_da_pessoa(url_0) 
    #_username_link = adicionar_pessoas_no_dicionario({}, amigos[0])
    usuarios = adicionar_nomes_no_dicionario(set(), amigos[0])
    contador = len(_username_link)
    num_max = 50000
    nos={}
    
    for individuo in amigos[0]:
        print(contador)
        
        if(contador >= num_max):
            break
        perfil = individuo.split('|||||')[0]
        link_perfil = individuo.split('|||||')[1]
        lista = buscar(perfil,link_perfil,contador,num_max,nos,perfis_varridos,set()) 
        nos.update(lista[0])
        contador = lista[1]
    
    _username_link.update(lista[2]) #conjunto na forma "{username}|||||{link}"
    perfis_varridos=lista[2] #conjunto que contém os perfis já olhados pelo programa
    return [nos,_username_link,perfis_varridos]
        
def escrever(nos):
    with open('conexoes.csv','w',encoding='utf-8') as arquivo:
        for user,friends in nos.items():
            print("a")
            for friend in friends:
                arquivo.write(f"{user}|||||{friend}\n")
    
    
url = "https://steamcommunity.com/profiles/76561199256402950/friends/"
url = "https://steamcommunity.com/id/sad_mablooM/friends"

_username_link = set()
nos,_username_link,perfis_varridos = arvore_de_conxoes(set(), url,_username_link)
tot = 0

lista = set()
for data in _username_link:
    try:    
        print(data.split('|||||')[0])
        url = data.split('|||||')[1]
        lista = arvore_de_conxoes(perfis_varridos, url, _username_link)
        nos.update(lista[0])
        lista.update(lista[1])
        perfis_varridos.join(lista[2])
    except:
        continue
escrever(nos)
grapho.grafico()




"""
pessoas = {} #guarda um dicionário, com a chave sendo o nome do usuário e o valor um link com sua pagina 
usuarios = set() #guarda o nome de todos os usuários
ligacoes = {} #guara um dicionário, onde a chave é o nome do usuario e o valor as pessoas as quais ele faz conexão
amigos = coletar_amigos_da_pessoa(url) #guarda uma lista com elementos neste formato: "{perfil_amigo}|||||{link_amigos_do_amigo}"
pessoas = adicionar_pessoas_no_dicionario(pessoas, amigos[0])
usuarios = adicionar_nomes_no_dicionario(usuarios, amigos[0])
contador = len(pessoas)
num_max = 500
perfis_varridos = set()

for individuo in amigos[0]:
    print(contador)
    
    if(contador >= num_max):
        break
    perfil = individuo.split('|||||')[0]
    link_perfil = individuo.split('|||||')[1]
    lista = buscar(perfil,link_perfil,contador,num_max,ligacoes,perfis_varridos) 
    ligacoes = lista[0]
    contador = lista[1]

for user,friends in ligacoes.items():
    print("-"*50,user,"-"*50)
    for friend in friends:
        print(friend)
        
"""