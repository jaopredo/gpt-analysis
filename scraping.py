import concurrent.futures

from functions.scraping.make_lists import make_steam_list
from functions.scraping.steam import steam
from functions.scraping.imdb import imdb

def scrap_from_web():
    # Criando a ista das empresas e dos jogos
    make_steam_list()
    

    # Raspando dados da Steam
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads_running = []

        threads_running.append(executor.submit(steam))
        threads_running.append(executor.submit(imdb))

        concurrent.futures.wait(threads_running)

