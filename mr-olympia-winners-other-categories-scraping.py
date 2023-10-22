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

# ------------ Classic Physique ----------------
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

# ------------ Men's 212 division ----------------
m_212_df = dfs[8]
m_212_df.head(3)

# raspando os países representados por cada atleta
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

m_212_df.insert(2, 'represented_country', rows)

# ------------ Men's Physique     ------------------
m_phy_df = dfs[9] # fazendo um dataframe com a tablea desejada

# raspando os países representados por cada atleta
table_m_phy = table[8]

rows = [] # cria a lista para armazenar os países
row_idx = 0 # cria uma variável para armazenar o índice do primeiro elemento da lista
for row in table_m_phy.find_all('tr')[1:]:
    value = row.find_all('td')
    
    if len(value) > 2:
        flag = value[2].find('a')['title']
    else:
        flag = rows[row_idx - 1] 

    rows.append(flag)
    row_idx += 1

# cria uma nova coluna à esquerda da coluna com os atletas campeões 
m_phy_df.insert(2, 'represented_country', rows)

# ------------  ----------------
CP_chronologically.to_csv('classic-physique-chrono.csv', index=False)
CP_top3.to_csv('classic-physique-top3.csv', index=False)
m_212_df.to_csv('mens-212.csv', index=False)
m_phy_df.to_csv('mens-physique.csv', index=False)

