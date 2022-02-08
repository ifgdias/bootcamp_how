#%%
# imports
import requests
import json

#%%

def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret = requests.get(url)
    cotacao = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{valor} {moeda[:3]} hoje custam {float(cotacao['bid']) * valor} {moeda[-3]}")


#%%

cotacao(20,'USD-BRL')

cotacao(100,'JPY-USD')

cotacao(100,'JPY-ISR')

# %%

lst_money = [
    'USD-BRL',
    'EUR-BRL',
    'BTC-BRL',
    'JPY-BRL',
    'RPL-BRL'
]
# %%
for moeda in lst_money:
    try:
        cotacao(20, moeda)
    except:
        print(f'Falha na moeda {moeda}')

#%%

dolar = jsx