##pip install prettytable
import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import pandas as pd
from decimal import Decimal



st.title(":blue[LI]:red[DOM] Temporada 2024-2025 :flag-do: :baseball:")
st.header("Tabla de Posiciones")

url = 'https://estadisticas.lidom.com/'
url2 = 'https://estadisticas.lidom.com/Colectivo'
respuesta = requests.get(url)
respuesta2 = requests.get(url2)

columns_standing = ["Equipo", "JJ", "G - P", "PCT", "JD","Casa", "Ruta", "Racha", "U10"]
columns_offensive_stats = ["Equipo","AVG", "OBP", "SLG", "OPS", "K%", "BB%"]
rows_standing = []
rows_offensive_stats = []
total_teams = 6

##aqui ponemos las estadisticas basicas
if respuesta.status_code == 200:
  soup = BeautifulSoup(respuesta.text, 'html.parser')
  soup2 = BeautifulSoup(respuesta2.text, 'html.parser')

  for x in range(total_teams):
    x += 1
    jj = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[1].get_text().strip()
    team_name = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[0].find_all('a')[0].get_text().strip()
    wins_loses = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[2].get_text().strip() + " - " + soup.find_all('table')[1].find_all('tr')[x].find_all('td')[3].get_text().strip()
    pct = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[4].get_text().strip()
    gb = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[5].get_text().strip()
    casa = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[6].get_text().strip()
    ruta = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[7].get_text().strip()
    racha = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[8].get_text().strip()
    u10 = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[9].get_text().strip()

    ##segundo
    team_name = soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[0].find_all('a')[0].get_text().strip()

    ab = int(soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[2].get_text().strip())
    k = int(soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[11].get_text().strip())
    bb = int(soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[9].get_text().strip())

    avg = (soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[15].get_text().strip())
    obp = (soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[16].get_text().strip())
    slg = (soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[17].get_text().strip())
    ops = (soup2.find_all('table')[1].find_all('tr')[x].find_all('td')[18].get_text().strip())

    pa = ab + bb

    k_rate = ((k/pa)*100)
    bb_rate = ((bb/pa)*100)


    k_rate = (format(k_rate,'.1f'))+"%"
    bb_rate = (format(bb_rate,'.1f'))+"%"

    rows_standing.append([team_name, jj, wins_loses, pct, gb, casa, ruta, racha, u10])
    rows_offensive_stats.append([team_name,avg,obp,slg,ops,k_rate,bb_rate])

df_standing = pd.DataFrame(rows_standing, columns=columns_standing)
df_offensive_stats = pd.DataFrame(rows_offensive_stats, columns=columns_offensive_stats)



st.dataframe(df_standing, width=2000, hide_index=True)
st.header("Estadísticas Ofensivas")
st.dataframe(df_offensive_stats, width=2000, hide_index=True)
