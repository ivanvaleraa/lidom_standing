##pip install prettytable
import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import pandas as pd


url = 'https://estadisticas.lidom.com/'
respuesta = requests.get(url)
columns = ["Equipo", "W - L", "PCT"]
##standing = PrettyTable(headers)

rows = []

if respuesta.status_code == 200:
  total_teams = 6
  soup = BeautifulSoup(respuesta.text, 'html.parser')

  for x in range(total_teams):
    x += 1
    team_name = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[0].find_all('a')[0].get_text().strip()
    wins_loses = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[2].get_text().strip() + " - " + soup.find_all('table')[1].find_all('tr')[x].find_all('td')[3].get_text().strip()
    pct = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[4].get_text().strip()
    rows.append([team_name,wins_loses,pct])

df = pd.DataFrame(rows, columns=columns)
df.set_index("Equipo", inplace=True)
# df.style.set_table_styles({
#     'Equipo': [{'selector': '',
#            'props': [('color','red'),('width', '200px')]}],
# }) not working
st.write(df)