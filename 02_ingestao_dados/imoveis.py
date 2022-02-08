#%%

#imports

from numpy import append
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import logging
import html5lib


# %%
url = 'https://www.vivareal.com.br/venda/minas-gerais/uberaba/apartamento_residencial/?pagina={}'


# %%
i = 1

ret = requests.get(url.format(i))

soup = bs(ret.text, "html5lib")

# %%
houses = soup.find_all(
    'a', {'property-card__content-link js-card-title'})

qty_houses = float(soup.find(
    'strong',{'results-summary__count js-total-records'}).text.replace('.',''))


# %%
len(houses)

# %%

qty_houses
# %%

house = houses[0]
house

#%%


house_info = []

i = 0

while qty_houses > len(house_info):

    i += 1

    print(f"posicao: {i} \t\t qtd_imoveis: {len(house_info)}")

    ret = requests.get(url.format(i))

    soup = bs(ret.text)

    houses = soup.find_all(
    'a', {'property-card__content-link js-card-title'})

    for house in houses:

        descricao = house.find('span', {
                    'class': 'property-card__title'}).text.strip()

        endereco = house.find('span', {
            'class':'property-card__address'}).text.strip(),

        area = house.find('span',{
            'class':'js-property-card-detail-area'}).text.strip(),

        quartos = house.find('li',{
            'class':'property-card__detail-room'}).span.text.strip(),

        wc = house.find('li',{
            'class':'property-card__detail-bathroom'}).span.text.strip(),

        vagas = house.find('li',{
            'class':'property-card__detail-garage'}).span.text.strip(),

        valor  = house.find('div',{
            'class':'property-card__price'}).p.text.strip(),
        
        try:
            condo = house.find('div',{
                'class':'property-card__price-details--condo'}).strong.text.strip(),
        except:
            condo = 0

        wlink = 'https://vivareal.com.br' + house['href']

        house_data = [
            descricao,
            endereco,
            area,
            quartos,
            wc,
            vagas,
            valor,
            condo,
            wlink
        ]

        house_info.append(house_data)


# %%

df = pd.DataFrame(
    house_info,
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'wc',
        'vagas',
        'valor',
        'condo',
        'wlink'
    ]
)

df

# %%

df.to_csv('scrap_vivareal_uberaba.csv', sep=';', index=False)
# %%
