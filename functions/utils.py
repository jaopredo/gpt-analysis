from time import time
import tiktoken

def see_execution_time(func, *args):
    """Decorator function to see the execution time of other functions
    """
    def slave(*args, **kwargs):
        initial_time = time()
        func(*args, *kwargs)
        end_time = time()
        
        print(f"A função demorou {end_time - initial_time} segundos")

    return slave


def get_number_of_tokens(sentence: any) -> int:
    """Calculate how much tokens a message will consume in the API
    """
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    return len(encoding.encode(str(sentence)))
