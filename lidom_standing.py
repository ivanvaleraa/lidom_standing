##pip install prettytable
import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import pandas as pd
from decimal import Decimal


url = 'https://estadisticas.lidom.com/'
url2 = 'https://estadisticas.lidom.com/Colectivo'
respuesta = requests.get(url)
respuesta2 = requests.get(url2)

columns = ["Equipo", "W - L", "PCT", "K%", "BB%"]
rows = []
total_teams = 6

##aqui ponemos las estadisticas basicas
if respuesta.status_code == 200:
  soup = BeautifulSoup(respuesta.text, 'html.parser')
  soup2 = BeautifulSoup(respuesta2.text, 'html.parser')

  for x in range(total_teams):
    x += 1
    team_name = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[0].find_all('a')[0].get_text().strip()
    wins_loses = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[2].get_text().strip() + " - " + soup.find_all('table')[1].find_all('tr')[x].find_all('td')[3].get_text().strip()
    pct = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[4].get_text().strip()

    ##segundo
    ab = int(soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[2].get_text().strip())

    k = int(soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[11].get_text().strip())
    bb = int(soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[9].get_text().strip())
    pa = ab + bb

    k_rate = ((k/pa)*100)
    bb_rate = ((bb/pa)*100)


    k_rate = (format(k_rate,'.1f'))+"%"
    bb_rate = (format(bb_rate,'.1f'))+"%"

    rows.append([team_name,wins_loses,pct,k_rate,bb_rate])

df = pd.DataFrame(rows, columns=columns)
df.set_index("Equipo", inplace=True)
# df.style.set_table_styles({
#     'Equipo': [{'selector': '',
#            'props': [('color','red'),('width', '200px')]}],
# }) not working
st.write(df)