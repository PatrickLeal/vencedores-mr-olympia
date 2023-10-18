# importando pacotes importantes
from bs4 import BeautifulSoup
import pandas as pd

# selenium 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

service = Service()
options = webdriver.ChromeOptions()
# options.add_argument('--headless')               # executar o código sem manter a página aberta
# options.add_argument('window-size=400,800')    # escolhendo o tamanho em que a página vai abrir
options.add_experimental_option("detach", True)

navegador = webdriver.Chrome(options=options, service=service) # instanciando o webdriver com alguns 'options' setados
navegador.get('https://en.wikipedia.org/wiki/Mr._Olympia#Medals')

sleep(2)

position_span = navegador.find_element(By.XPATH,
                                       '//*[contains(concat( " ", @class, " " ), concat( " ", "headerSort", " " ))]')
navegador.implicitly_wait(2)
position_span.click()

page = BeautifulSoup(navegador.page_source, 'html.parser')

table = page.find("table", {"class": "wikitable sortable jquery-tablesorter"})

# selecionando os headers das colunas
headers = [header.text.strip() for header in table.find_all('th')]

rows = [] # cria uma lista vazia para armazenar as linhas da tabela
for row in table.find_all('tr')[1:]: 
    value = row.find_all('td')                             # salva os valores da linha atual

    beautified_value = [ele.text.strip() for ele in value] # salva cada elemento individualmente da linha atual em uma lista

    if len(beautified_value) == 0:                         # remove os data arrays que estão vazios
        continue
    
    rows.append(beautified_value)                          # faz o append da linha na lista 'rows'

# checa se a quantidade de itens da linha é maior que a quantidade de headers
for r in rows:
    if len(r) > 5:
        r[2] = r[2] + " - " + r[3] # concatena o 3° e 4° item da linha no 3° item
        r.pop(3)                   # remove o 4° item da linha

df = pd.DataFrame(rows, columns=headers)                   # salva em um dataframe
df = df.drop(columns='#')                                  # remove a coluna '#'

# salva em um arquivo csv
df.to_csv('mr-olympia-winners.csv', index=False)