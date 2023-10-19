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
options.add_argument('--headless')               # executar o código sem manter a página aberta
# options.add_argument('window-size=400,800')    # escolhendo o tamanho em que a página vai abrir
options.add_experimental_option("detach", True)  # impede a página de fechar automaticamente após abrir

navegador = webdriver.Chrome(options=options, service=service) # instanciando o webdriver com alguns 'options' setados
navegador.get('https://en.wikipedia.org/wiki/Mr._Olympia#')

sleep(2)

page = BeautifulSoup(navegador.page_source, 'html.parser')

table = page.find_all("table", {"class": "wikitable sortable jquery-tablesorter"})
table_top3 = table[3] # salvando somente a tablea que eu vou raspar

rows = [] # cria uma lista vazia para armazenar as linhas da tabela
for row in table_top3.find_all('tr')[1:]: 
    value = row.find_all('td')                             # salva os valores da linha atual
    
    representing = []
    # como algumas células estão vazias, eu precisei criar esse tratamento de exceção
    try:
        # Encontrar o nome do país com a tag 'a' se existir
        for i in range(1, 4):
            flag = value[i].find('a')['title']
            representing.append(flag)

    except Exception as error:
        # salvando o país do campeão porque sempre há a ocorrência do mesmo dentro da tabela
        flag = value[1].find('a')['title']
        representing.append(flag)
                
    beautified_value = [ele.text.strip() for ele in value] # salva cada elemento individualmente da linha atual em uma lista

    if len(beautified_value) == 0:                         # remove os data arrays que estão vazios
        continue
    
    # colocando os nomes dos países a esquerda do nome do atleta
    for i in range(len(representing)):
        idx = 2 * i + 1
        beautified_value.insert(idx, representing[i])
    
    rows.append(beautified_value)                          # faz o append da linha na lista 'rows'

# criando headers para o DataFrame
headers = ['Year', 'represented_country_cham', 'Champion',
         'represented_country_runn', 'Runner-Up',
         'represented_country_thir', '3rd Place']

df = pd.DataFrame(rows, columns=headers)

# limpando alguns erros gerados na seguintes linhas
df['represented_country_runn'][3] = ''
df['represented_country_thir'][4] = ''
df['represented_country_runn'][6] = ''

# salva em um arquivo csv
df.to_csv('mr-olympia-winners-top-positions.csv', index=False)
