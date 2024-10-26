##pip install prettytable
import os
import requests
import streamlit as st
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

st.set_page_config(layout="wide")


bref = 'https://www.baseball-reference.com/register/league.cgi?id=3d6041f6'
r = requests.get(bref)
soup = BeautifulSoup(r.content, "html.parser")

st.title(":blue[LI]:red[DOM] Temporada 2024-2025 :flag-do::baseball:")
st.header("Estadísticas por Equipo")
st.subheader("Tabla de Posiciones")

##aqui ponemos las estadisticas basicas
if r.status_code == 200:
  standing = pd.DataFrame(pd.read_html([StringIO(soup.extract()) for soup in soup.find_all(string=lambda text: isinstance(text, Comment)) if 'id="div_standings_pitching"' in soup][0])[0])
  standing['J'] = standing['W']+standing['L']
  standing = standing[['Tm','J','W','L','W-L%','GB']]
  standing = standing.rename(columns={'Tm':'Equipo','W':'G','L':'P','W-L%':'Pct%','GB':'Dif'})
  formatted_standing = standing.style.format({"Pct%": "{:.3f}".format})
  st.dataframe(formatted_standing, width=2000, hide_index=True)
  offensive_stats = pd.DataFrame(pd.read_html([StringIO(soup.extract()) for soup in soup.find_all(string=lambda text: isinstance(text, Comment)) if 'id="div_league_batting"' in soup][0])[0])
  offensive_stats = offensive_stats.drop(['Aff','BatAge','TB','GDP','HBP','SH','SF','IBB','SB','CS','G'], axis=1)
  offensive_stats['K%'] = offensive_stats['SO']/offensive_stats['PA']
  offensive_stats['BB%'] = offensive_stats['BB']/offensive_stats['PA']
  offensive_stats = offensive_stats.rename(columns={'Tm':'Equipo','R/G':'C/J'})
  offensive_stats = offensive_stats[:-1]
  mapper =  {'C/J': '{0:.2f}',
           'BA': '{0:.3f}',
           'OBP': '{0:.3f}',
           'SLG': '{0:.3f}',
           'OPS': '{0:.3f}',
           'K%': '{0:.2f}%',
           'BB%': '{0:.2f}%'}
  formatted_offensive_stats = offensive_stats.style.format(mapper)
  st.subheader("Estadísticas Ofensivas")
  st.dataframe(formatted_offensive_stats, width=2000, hide_index=True)
