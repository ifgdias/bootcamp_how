#%%

from cgi import test
from time import asctime
import requests
import json


# %%

def error_check(func):
    def inner_func(*args,**kwargs):
        try:
            func(*args,**kwargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func


@error_check
def cotacao(valor, moeda):

    url = f'https://economia.awesomeapi.com.br/last/{moeda}'

    ret = requests.get(url)

    cotacao = json.loads(ret.text)[moeda.replace('-','')]

    print(f"{valor} {moeda[:3]} hoje custam {float(cotacao['bid']) * valor} {moeda[-3:]}")

#%%

cotacao(20,'USD-BRL')
cotacao(20,'EUR-BRL')
cotacao(20,'BTC-BRL')
cotacao(20,'JPY-BRL')
cotacao(20,'RPL-BRL')

# %%
import backoff
import random

# %%

@backoff.on_exception(backoff.expo, (
    ConnectionAbortedError,ConnectionRefusedError,TimeoutError), max_tries=10)
def test_func(*args,**kwargs):

    rnd = random.random()

    print(f"""
        RND : {rnd}
        args: {args if args else 'sem args'}
        kwargs: {kwargs if kwargs else 'sem kwargs'}
    """)

    if rnd < .2:
        raise(ConnectionAbortedError('Conexão foi finalizada'))
    elif rnd < .4:
        raise(ConnectionRefusedError('Conexão recusada'))
    elif rnd < .6:
        raise(TimeoutError('Tempo de espera excedido'))
    else:
        return 'OK!'

# %%
test_func()

# %%
import logging

#%%
log = logging.getLogger()

log.setLevel(logging.INFO)

FORMAT = "%(asctime)s %(name)s %(message)s"

formatter = logging.Formatter(FORMAT)

ch = logging.StreamHandler()

ch.setFormatter(formatter)

log.addHandler(ch)


# %%

@backoff.on_exception(backoff.expo, (
    ConnectionAbortedError,ConnectionRefusedError,TimeoutError), max_tries=10)
def test_func(*args,**kwargs):

    rnd = random.random()

    log.debug(f"RND : {rnd}")
    log.info(f"args: {args if args else 'sem args'}")
    log.info(f"kwargs: {kwargs if kwargs else 'sem kwargs'}")
        
    if rnd < .2:
        log.error('Conexão foi finalizada')
        raise(ConnectionAbortedError('Conexão foi finalizada'))
    elif rnd < .4:
        log.error('Conexão recusada')
        raise(ConnectionRefusedError('Conexão recusada'))
    elif rnd < .6:
        log.error('Tempo de espera excedido')
        raise(TimeoutError('Tempo de espera excedido'))
    else:
        return 'OK!'
# %%
test_func()

# %%

url2 = 'https://portalcafebrasil.com.br/todos/podcasts/'

ret2 = requests.get(url2)
#%%
ret2.text

# %%

from bs4 import BeautifulSoup as bs

# %%

url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

url.format(5)

#%%

def get_podcasts(url):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all('h5')

# %%
get_podcasts(url.format(6))

#%%

import logging

#%%

log = logging.getLogger()
log.setLevel(logging.DEBUG)
FORMAT ='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(FORMAT)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

#%%

i = 1

lst_get = get_podcasts(url.format(i))


#%%

lst_podcasts = []

while len(lst_get) > 0:

    lst_podcasts = lst_podcasts + lst_get
    lst_get = get_podcasts(url.format(i))
    log.debug(f"Coletados {len(lst_get)} episodios do link {url.format(i)}")

    i += 1


# %%
len(lst_podcasts)
# %%

import pandas as pd

# %%

df = pd.DataFrame(columns=['nome','link'])
# %%
for item in lst_podcasts:
    df.loc[df.shape[0]] = [item.text,item.a['href']]
# %%

df.shape
# %%
df
# %%
df.to_csv('podcasts.csv',sep=';',index=False)
# %%
