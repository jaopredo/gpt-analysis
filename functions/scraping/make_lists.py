"""
Module that consults with gpt chat and generates the companies and games database
"""
import configs
from ai import client
import re
    

def make_steam_list():
    """
        Crete file csv with especify formated for steam games    
    """

    with open('data/steam_list.csv', mode='w', newline='', encoding='utf-8') as file:
        gpt_message = f""" Hi, Please return a list with {configs.COMPANIES_QUANTITY} companies, along with five games from the company that are on Steam. The response must STRICTLY FOLLOW THIS FORMAT:

        COMPANY1||||GAME 1||||GAME 2||||GAME 3||||GAME 4||||GAME 5"/n"COMPANY2||||GAME 1||||GAME 2||||GAME 3||||GAME 4||||GAME 5"/n"COMPANY3||||GAME 1||||GAME 2||||GAME 3||||GAME 4||||GAME 5"/n"
        
        IMPORTANT: DO NOT INCLUDE TABS, TITLE, QUOTES, OR A LIST COUNTER IN THE RESPONSE. THE RESPONSE SHOULD ONLY CONTAIN THE CODE BLOCK
        """



        prompt = [{"role": "user", "content": f"{gpt_message}"}]        
        response = client.chat.completions.create(
            messages = prompt,
            model = "gpt-3.5-turbo-0125",
            temperature=0
        ) 

        file.write(response.choices[0].message.content)
