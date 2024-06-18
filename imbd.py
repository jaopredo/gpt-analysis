import requests
from bs4 import BeautifulSoup
import re

url = "https://www.google.com/search?q=the+last+of+us+game+imdb&newwindow=1&sca_esv=07dd5598d35cffb5&sxsrf=ADLYWIJLL_lJ8xreXvKC30uH4IGmBKIWWg%3A1718575320335&ei=2GBvZpWKFOnN1sQPp46egA0&ved=0ahUKEwiV1vP7j-GGAxXpppUCHSeHB9AQ4dUDCBA&uact=5&oq=the+last+of+us+game+imdb&gs_lp=Egxnd3Mtd2l6LXNlcnAiGHRoZSBsYXN0IG9mIHVzIGdhbWUgaW1kYjIIEAAYgAQYywEyBRAAGIAEMgYQABgIGB4yBhAAGAgYHjIGEAAYCBgeMgsQABiABBiGAxiKBTILEAAYgAQYhgMYigUyCxAAGIAEGIYDGIoFMgsQABiABBiGAxiKBTILEAAYgAQYhgMYigVI1SBQhAdYpwtwAXgBkAEAmAGYA6ABjQiqAQkwLjEuMi4wLjG4AQPIAQD4AQGYAgKgAokCwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAhYQLhiABBiwAxhDGNQCGMgDGIoF2AEBwgITEC4YgAQYsAMYQxjIAxiKBdgBAZgDAIgGAZAGFLoGBggBEAEYCJIHBTEuMC4xoAeFIQ&sclient=gws-wiz-serp"
url = "https://www.google.com.br/search?q=diablo+III+imdb&newwindow=1&sca_esv=c8a309c0fc9cf8f6&sxsrf=ADLYWIL8ZjcEmpjuAXli4Kna3Uw67ylSFw%3A1718576999642&ei=Z2dvZvHcJpHe1sQPwZ6osAQ&ved=0ahUKEwixrNScluGGAxURr5UCHUEPCkYQ4dUDCBA&uact=5&oq=diablo+III+imdb&gs_lp=Egxnd3Mtd2l6LXNlcnAiD2RpYWJsbyBJSUkgaW1kYjIFEAAYgAQyBhAAGBYYHjILEAAYgAQYhgMYigUyCxAAGIAEGIYDGIoFMggQABiABBiiBEi0EVDAAlicDnABeAGQAQCYAfwBoAHlBqoBBTAuNC4xuAEDyAEA-AEBmAIGoAKmB8ICChAAGLADGNYEGEfCAg0QABiABBiwAxhDGIoFwgIOEAAYsAMY5AIY1gTYAQHCAhMQLhiABBiwAxhDGMgDGIoF2AECwgIWEC4YgAQYsAMYQxjUAhjIAxiKBdgBAsICCBAuGIAEGMsBwgIIEAAYgAQYywHCAhcQLhiABBjLARiXBRjcBBjeBBjgBNgBA8ICChAAGIAEGBQYhwKYAwCIBgGQBhO6BgYIARABGAm6BgYIAhABGAi6BgYIAxABGBSSBwUxLjQuMaAHkiE&sclient=gws-wiz-serp"
def pegar_link_comentario(jogos):
    """
    pega o link do imdb do jogo quando pesquisado no google
    """
    links = []
    for url in jogos:
        page = requests.get(url)
        fatia = BeautifulSoup(page.text, "lxml")
        fat = fatia.find("div", class_="egMi0 kCrYT")
        link = fat.find("a")['href']
        limpo = re.search(r'/url\?q=(.+?)&sa=U',link)
        links.append(limpo.group(1) + "reviews/?ref_=tt_ov_rt")
    return links
#print(pegar_link_comentario(url))

def pega_lista_jogos():
    """
    pega os jogos do arquivo lista_games.txt
    """
    i = 1
    jogos = []
    with open('lista_games.txt', 'r') as arquivo:
        for jogo in arquivo:
            jogos.append(jogo)
            i+=1
            if(i >=100):
                break
    return jogos

def pesquisa_google(jogos):
    links= []
    for jogo in jogos:    
        jogo = re.sub(r' ', '+',jogo)
        links.append(f"https://www.google.com.br/search?q={jogo}+game+imdb")
    return links

jogos = pega_lista_jogos()
jogos = pesquisa_google(jogos)
jogos = pegar_link_comentario(jogos)
print(jogos)
i = 1
for jogo in jogos:
    try:
        with open('abcd.txt', 'a') as arquivo:
            page = requests.get(jogo)
            print(f"passou por {i} jogos")
            soup = BeautifulSoup(page.text, "lxml")
            lista = soup.find_all("div", class_="lister-item-content")
            for comentario in lista:
                arquivo.write(comentario.text.strip())
            i+=1
    except:
        continue