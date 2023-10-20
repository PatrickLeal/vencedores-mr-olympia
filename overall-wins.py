import pandas as pd
import requests

# para debug
from icecream import ic

# URL da página da Wikipedia
url = 'https://en.wikipedia.org/wiki/Mr._Olympia#Medals'

# Enviar uma solicitação GET para a página
response = requests.get(url)
# ic(response.status_code)

# criando uma lista com as tabelas no html
dfs = pd.read_html(response.text)

# salvando somente a tabela desejada
overall_df = dfs[2]

# removendo as colunas multi-niveis
overall_df.columns = overall_df.columns.droplevel(0)

# salvando em um arquivo csv
overall_df.to_csv('number-of-overall-wins.csv', index=False)