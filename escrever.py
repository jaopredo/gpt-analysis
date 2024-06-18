import steam
import threading
import playstation
import os

os.system("cls")

def steam_commentary():
    games = steam.steam()
    with open('steam.csv', 'w', encoding = 'utf-8') as tabela:
        tabela.write("TITLE;USER_NAME;USER_GAMES;GENERAL_OPINION_OF_PEOPLE;FINAL_OPINION;COMMENTARY;DATE"+"\n")
    
    print(games)
    for game_list in games:
        with open('steam.csv', 'a', encoding ='utf-8' ) as tabela:
            for value in game_list.values():
                try:
                    for commentary in value['commentary'].values():
                        tabela.write(value['title']+';')
                        for text in commentary.values():
                            tabela.write(text+";")
                        tabela.write("\n")
                except:
                        continue
    
def playstation_commentary():
    games = playstation.playstation()
    
    with open ('playstation.csv', 'w', encoding = 'utf-8') as arquivo:
        arquivo.write("TITLE;\n")
        for key in games.items():
            try:
                arquivo.write(key+";\n")
            except:
                continue
thread_steam = threading.Thread(target = steam_commentary)
thread_playstation = threading.Thread(target = playstation_commentary)

thread_steam.start()
thread_playstation.start()
