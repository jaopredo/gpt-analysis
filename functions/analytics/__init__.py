import concurrent.futures
from ai import client
import pandas as pd
from functions.utils import *
import unicodedata
import configs
import json
import openai
from time import sleep


def get_comment_scale(comments: str, n: int) -> list[dict]:
    """Função específica para realizar a ponte entre o CHATGPT e a conversão do comentário para uma escala de 0 a 10. Ela pega o comentário, manda pro GPT, retorna o valor e esse valor é adicionado na lista passada
    :param comment: Comentário pedido
    :param comments_on_scale_column: Lista com todas as notas
    """
    try:
        response: str = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"See this list of comments, convert them in a scale from 0 to 10, I want you to return only a JSON list of dictionaries, each one have an \'id\' key, you must not change it from the original, and a \'rate key\' with the number you calculated :\n \'{comments}\'"
                },
            ],
            model="gpt-3.5-turbo",
            temperature=0
        )
        print(f"{n} calculada")

        return json.loads(response.choices[0].message.content)  # Adicionando comentários no json
    except openai.OpenAIError as e:  # Se o chatgpt retornar um erro de tokens
        print('\n\n =================================')
        print(f"Erro na {n}, tentando calcular novamente!")
        print(' ================================= \n\n')
        print(e)
        sleep(5)  # Espero 10 segundos
        return get_comment_scale(comments, n)  # Tento executar novamente a função


def minimise_tokens_per_message(comments: pd.Series) -> list[dict]:
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
    """Função que analisa os comentários
    :param dataframe: Dataframe do pandas que será alterado
    """

    comments_on_scale: list[dict] = []  #  A Lista que vai ter as notas em dicionários
    
    # Mando a coluna com os comentários para a função que vai retornar uma lista separada para que
    # Não envie tantos comentários ao mesmo tempo
    comments_to_send_to_gpt = minimise_tokens_per_message(dataframe['COMENTARIO'])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads_executing: list[concurrent.futures.Future] = []  # Threads executadas

        for i, comment_to_send in enumerate(comments_to_send_to_gpt):  # Pra cada lista de dicionários dentro da lista principal
            threads_executing.append(executor.submit(get_comment_scale, comment_to_send, i))

        concurrent.futures.wait(threads_executing)  # Espero todos os comentários serem processados

        # Lista temporária que irá servir para organizar os cometários que foram retornados
        comments_on_scale_to_convert = []

        for thread in threads_executing:
            comments_on_scale_to_convert += thread.result()
        
    for comment in sorted(comments_on_scale_to_convert, key=lambda d: d['id']):
        comments_on_scale.append(comment['rate'])
    
    dataframe['COMENTARIO_COMO_NOTA'] = comments_on_scale
