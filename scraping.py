from functions.scraping.make_lists import make_steam_list
from functions.scraping.steam import steam
from functions.scraping.imdb import imdb

def scrap_from_web():
    # Criando a ista das empresas e dos jogos
    make_steam_list()
    

    # Raspando dados da Steam
    steam()
    
    # Raspando dados do IMDB
    imdb()
