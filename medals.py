# importando pacotes importantes
from bs4 import BeautifulSoup
import pandas as pd
import requests

# para debug
from icecream import ic

# URL da página da Wikipedia
url = 'https://en.wikipedia.org/wiki/Mr._Olympia#Medals'

# Enviar uma solicitação GET para a página
response = requests.get(url)
# ic(response.status_code)

page = BeautifulSoup(response.text, 'html.parser')

# Encontrar a minha tabela desejada
tables = page.find_all("table", class_="wikitable sortable")
medal_table = tables[4] # salvando somente a tablea que eu vou usar

# selecionando os headers das colunas
headers = [header.text.strip() for header in medal_table.find_all('th')]
headers

rows = []
for row in medal_table.find_all('tr')[1:]:
    value = row.find_all('td')

    beautified_value = [ele.text.strip() for ele in value] # salva cada elemento individualmente da linha atual em uma lista

    if len(beautified_value) == 0:                         # remove os data arrays que estão vazios
        continue

    rows.append(beautified_value)                          # faz o append da linha dentro da lista de linhas


df = pd.DataFrame(rows, columns=headers)

# removendo tudo que está dentro dos [] nos nomes das colunas
df.columns = df.columns.str.replace(r'\[[^\]]*\]', '', regex=True)
df.to_csv('medals.csv', index=False)