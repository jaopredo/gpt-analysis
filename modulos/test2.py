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
    fatia = soup.find("div", class_="egMi0 kCrYT")
    link = fatia.find("a")
    link = link['href']
    id_jogo = re.search(r'/sub/(\d+)', link).group(1)
    link = f"https://store.steampowered.com/app/{id_jogo}"
    #print(link)
    return [id_jogo,link]    #retorna o link do jogo na Steam para o programa


print(pesquisa_google("Grand Theft Auto: The Trilogy - The Definitive Edition steam"))
