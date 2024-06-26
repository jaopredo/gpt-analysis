"""
This module has the functions responsible for sending the comments for CHATGPT and transforming them into a rate between 0 and 10
"""

import concurrent.futures
from ai import client
import pandas as pd
from functions.utils import *
import unicodedata
import configs
import json
import openai
from time import sleep


def get_comment_scale(comment: str, n: int) -> list[dict]:
    """Função específica para realizar a ponte entre o CHATGPT e a conversão do comentário para uma escala de 0 a 10. Ela pega o comentário, manda pro GPT, retorna o valor e esse valor é adicionado na lista passada
    :param comment: Comentário pedido
    :param comments_on_scale_column: Lista com todas as notas
    """
    try:
        print(f"{n} sendo calculado")
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"See this comment and transform it in a scale from 0 to 10, if the comment doesn't make sense, return 0. I want you to return just one number, nothing more :\n \'{comment}\'"
                },
            ],
            model="gpt-3.5-turbo",
            temperature=0
        )
        print(f"{n} calculada")
        print(response.choices[0].message.content)

        return float(response.choices[0].message.content)  # returning the comment converted in a note
    except openai.OpenAIError as e:  # If GPT gives an error
        print('\n\n =================================')
        print(f"Erro na {n}, tentando calcular novamente!")
        print(' ================================= \n\n')
        print(e)
        sleep(5)  # Wait 5 seconds
        return get_comment_scale(comment, n)  # Try to call the function again


def minimise_tokens_per_message(comments: pd.Series) -> list[dict]:
    """This function was responsible for getting all the comments and dividing them in sublists based on how
    many tokens they would use, using a permanent variable to do so. This function is not used anymore,
    because it was causing some hard fixing issues with CHATGPT, so we decided to remove it. We didn't erease
    it because we thought it could be useful again
    :param comments: The pandas series with the comments
    """
    raise DeprecationWarning
    total_tokens = get_number_of_tokens(list(comments))  # Quantos tokens vão ser enviados
    minimum_interations = total_tokens // configs.TOKENS_LIMIT  # Em quantos tokens vou ter que dividir

    comments_to_send_to_gpt: list[list[dict]] = []

    wich_list = 0  # Qual lista está sendo alterada dentro de comments_to_send_to_gpt
    actual_tokens_count = 0  # Quantos tokens as mensagens estão acumulando
    for i, cmnt in enumerate(comments):
        if i == 0:
            comments_to_send_to_gpt.append([])

        actual_tokens_count += get_number_of_tokens(cmnt)  # Adiciono a quantidade de tokens no número

        # Se a contagem for maior que o limite
        if actual_tokens_count >= configs.TOKENS_LIMIT:
            comments_to_send_to_gpt.append([])  # Crio mais uma lista
            wich_list += 1  # Digo que vou adicionar na próxima lista
            actual_tokens_count = 0  # Zero a contagem de tokens
        
        # Adiciono o comentário
        comments_to_send_to_gpt[wich_list].append({ 'id': i, 'comment': cmnt })
    
    return comments_to_send_to_gpt  # Retorno minha lista


# Função que transforma a avaliação do comentário em uma escala numérica
@see_execution_time
def analyse_comments(dataframe: pd.DataFrame) -> None:#
    """Function responsible for passing the comments to another function that will convert the comments as
    notes in a scale from 0 to 10
    :param dataframe: Dataframe do pandas que será alterado
    """

    comments_on_scale: list[float] = []  #  List that will be the new dataframe column

    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads_executing: list[concurrent.futures.Future] = []  # Threads executing

        for i, comment_to_send in enumerate(dataframe['COMMENT']):  # For each comment in the dataframe
            threads_executing.append(executor.submit(get_comment_scale, comment_to_send, i))
            # Append the thread running in the list
            # Send the function to the thread executor

        concurrent.futures.wait(threads_executing)  # Wait all comments be processed

        for thread in threads_executing:  # Add the results to the new column list (comments_on_scale)
            comments_on_scale += [thread.result()]
    
    dataframe['COMMENT AS NOTE'] = comments_on_scale
