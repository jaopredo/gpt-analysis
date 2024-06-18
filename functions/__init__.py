import asyncio
from ai import client
import pandas as pd
from functions.utils import see_execution_time
import threading

def comment_to_scale_gpt_call(comment, comments_on_scale_column):
    """
    Função específica para realizar a ponte entre o CHATGPT e a conversão do comentário para uma escala de 0 a 10
    """
    response = client.chat.completions.create(messages=[
        {
            "role": "user",
            "content": f"Por favor, faça a análise de um comentário e o converta para uma escala de 0 à 10, se o comentário não tiver nexo, retorne 5, não esqueça de retornar APENAS um número, sem nenhum outro texto: '{comment}'"
        },
    ], model="gpt-3.5-turbo", max_tokens=100, temperature=1)

    comments_on_scale_column.append(response.choices[0].message.content)


# Função que transforma a avaliação do comentário em uma escala numérica
@see_execution_time
def comment_to_scale(dataframe: pd.DataFrame):
    running_threads = []
    comments_on_scale_column = []

    for i, comment in enumerate(dataframe['COMMENTARY']):
        t = threading.Thread(target=comment_to_scale_gpt_call, args=(comment, comments_on_scale_column))
        t.start()
        running_threads.append(t)
    
    for thread in running_threads:
        thread.join()
    
    print(comments_on_scale_column)
