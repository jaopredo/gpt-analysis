"""
This module has the functions responsible for making a GPT analysis about the pc specs for running the game
"""

import pandas as pd
import concurrent.futures
from ai import client
import openai


def make_requisites_analysis(requisites, recommended):
    """This function receives two strings, one tells the minimum requisites for running the game, and the
    other the recommended setup for running the game without LAG. It passes this parameters to CHATGPT and
    it returns an analysis about the price of a PC with the corresponded passed setup.
    :param requisites: Minimum requisites
    :param recommended: Recommended setup
    """
    try:  # Try to send it to CHATGPT
        requisites_response = client.chat.completions.create(  # Send the minimum requisites text
            messages=[
                {
                    "role": "user",
                    "content": f"Please, see this PC components and estipulate how much a computer with this specifications would cost. Return a really small text about the components prices too, return in Brazilian Reais: {requisites}"
                },
            ],
            model="gpt-3.5-turbo",
            temperature=0
        )

        recommended_response = client.chat.completions.create(  # Send the recommended setup
            messages=[
                {
                    "role": "user",
                    "content": f"Please, see this PC components and estipulate how much a computer with this specifications would cost. Return a really small text about the components prices too, return in Brazilian Reais: {recommended}"
                }
            ],
            model="gpt-3.5-turbo",
            temperature=0
        )

        print("Informações de requisitos CARREGADA")  # Show that the informations were successfully loaded

        return (  # Return CHATGPT responses
            requisites_response.choices[0].message.content,
            recommended_response.choices[0].message.content
        )

    except openai.OpenAIError as e:  # If that is an error, try to execute the function again after 5 seconds
        print('\n\n =================================')
        print(f"Erro calculando as informações de especificação, tentando calcular novamente!")
        print(' ================================= \n\n')
        print(e)
        sleep(5)  # Wait 5 seconds
        return make_requisites_analysis(requisites, recommended)  # Try to call the function again


def generate_requisites_analysis(games_df: pd.DataFrame):
    """This function receives a dataframe with all the games that were obtained in the webscraping, gets the
    minimum requisites and the recommended setup for that games and passes to a function that analyse them
    with CHATGPT.
    :param games_df: The games dataframe
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:  # Structure for multithreading
        threads_executing = []

        for game in games_df.iterrows():  # Analyse all games
            threads_executing.append(
                executor.submit(  # Function and it's arguments (Send to the thread executor)
                    make_requisites_analysis,
                    game[1]["MINIMUM REQUIREMENTS"],
                    game[1][" RECOMMENDED REQUIREMENTS"]
                )
            )
        
        concurrent.futures.wait(threads_executing)  # Wait for all requisites be analysed
 
        # Lists that will be the games dataframe COLUMN
        requisites_gpt_analysis = []
        recommended_gpt_analysis = []

        for pending_thread in threads_executing:  # For thread executed in the list
            result = pending_thread.result()  # Get the thread result
            requisites_gpt_analysis.append(result[0])  # Append the returns to the corresponding column
            recommended_gpt_analysis.append(result[1])
        
        games_df['GPT MINIMUM REQUIREMENTS ANALYSIS'] = requisites_gpt_analysis
        games_df['GPT RECOMMENDED REQUIREMENTS ANALYSIS'] = recommended_gpt_analysis
