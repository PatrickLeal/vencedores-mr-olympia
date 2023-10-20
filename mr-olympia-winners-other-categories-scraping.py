from bs4 import BeautifulSoup
import pandas as pd
import requests
from icecream import ic  # para debug


# URL da página da Wikipedia
url = 'https://en.wikipedia.org/wiki/Mr._Olympia#Medals'

# Enviar uma solicitação GET para a página
response = requests.get(url)

# criando uma lista com as tabelas no html
dfs = pd.read_html(response.text)

CP_chronologically = dfs[6]
CP_top3 = dfs[7]

page = BeautifulSoup(response.text, 'html.parser')

table = page.find_all("table", class_="wikitable sortable")
table_top3 = table[5]   # salvando somente a tablea que eu vou raspar

rows = []
for row in table_top3.find_all('tr')[1:]:
    value = row.find_all('td')

    representing = []
    # Encontrar o nome do país com a tag 'a' se existir
    for i in range(1, 4):
        flag = value[i].find('a')['title']
        representing.append(flag)

    rows.append(representing)

headers =  ['represented_country_cham', 'represented_country_runn', 'represented_country_thir']
represented_country_df = pd.DataFrame(rows, columns=headers)

# adicionando as colunas com os nomes dos países na tabela com os top 3 Classic Physique
CP_top3.insert(1, represented_country_df.columns[0], represented_country_df.iloc[:, 0])
CP_top3.insert(3, represented_country_df.columns[1], represented_country_df.iloc[:, 1])
CP_top3.insert(5, represented_country_df.columns[2], represented_country_df.iloc[:, 2])

CP_chronologically.head(3)
CP_top3.head(3)

# ------------ Men's 212 division ----------------
m_212_df = dfs[8]
m_212_df.head(3)

table = page.find_all("table", class_="wikitable")
table_212 = table[7]

rows = []
row_idx = 0
for row in table_212.find_all('tr')[1:]:
    value = row.find_all('td')
    
    if len(value) > 2:
        flag = value[2].find('a')['title']
    else:
        flag = rows[row_idx - 1] 

    rows.append(flag)
    row_idx += 1

# removendo o primeiro item da lista 2 vezes porque 
# foi salvo 2 vezes a mais
rows.pop(0)
rows.pop(0)

m_212_df.insert(2, 'represented_country', rows)
m_212_df

# ------------ Men's Physique     ------------------