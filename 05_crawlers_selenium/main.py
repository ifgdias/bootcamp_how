#%%

from selenium import webdriver
import sys
# %%

cep = sys.argv[1]

if cep:

    driver = webdriver.Firefox()
    # %%

    driver.get(
        'https://buscacepinter.correios.com.br/app/endereco/index.php?t')

    elem_cep = driver.find_element_by_name('endereco')
    elem_cep

    #%%

    elem_cep.send_keys(cep)

    #%%

    elem_tipo_cep = driver.find_element_by_name('tipoCEP')
    elem_tipo_cep.click()

    driver.find_element_by_xpath(
        '/html/body/main/form/div[1]/div[1]/div/div[2]/div/div[2]/select/option[1]'
    ).click()

    driver.find_element_by_id(
        'btn_pesquisar'
    ).click()

    #%%


    # %%

    logradouro = driver.find_element_by_xpath(
        '/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr[1]/td[1]'
    ).text

    bairro = driver.find_element_by_xpath(
        '/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr[1]/td[2]'
    ).text

    localidade = driver.find_element_by_xpath(
        '/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr[1]/td[3]'
    ).text

    cep = driver.find_element_by_xpath(
        '/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr[1]/td[4]'
    ).text

    driver.close()
    # %%

    print("""
    Para o CEP {}, temos:
    Endereço: {}
    Bairro: {}
    Localidade: {}
    """.format(
        cep, logradouro, bairro, localidade
    ))

# %%
