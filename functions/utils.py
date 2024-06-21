from time import time
import tiktoken

def see_execution_time(func, *args):
    def slave(*args, **kwargs):
        initial_time = time()
        func(*args, *kwargs)
        end_time = time()
        
        print(f"A função demorou {end_time - initial_time} segundos")

    return slave


def get_number_of_tokens(sentence: any) -> int:
    """Calcula a quantidade de tokens que a API vai usar
    """
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    return len(encoding.encode(str(sentence)))


def get_comment_as_dict(ids, rate):
    print(ids, rate)
    return { 'id': ids, 'rate': rate }
