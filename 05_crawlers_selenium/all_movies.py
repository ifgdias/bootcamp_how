#%%

from selenium import webdriver
import time
import pandas as pd

# %%
driver = webdriver.Firefox()
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')

time.sleep(3)

tabela = driver.find_element_by_xpath(
    '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]'
)

# %%
df = pd.read_html(
    '<table>' + tabela.get_attribute('innerHTML') + '</table>'
    )[0]
df

# %%
df.columns
# %%

df[df['Ano']==1984]

# %%
df.to_csv('filmes_nicolas_cage.csv', sep=';', index=False)
# %%
