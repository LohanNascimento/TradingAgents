# utils/helpers.py 

def batcher(iterable, n):
    """Divide uma lista em batches de tamanho n."""
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n] 