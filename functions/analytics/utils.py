
def get_number_of_tokens(sentence: any) -> int:
    """Calcula a quantidade de tokens que a API vai usar
    """
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    return len(encoding.encode(str(sentence)))
