##pip install prettytable
import os
import requests
import streamlit as st
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO
import matplotlib

st.set_page_config(layout="wide")


bref = 'https://www.baseball-reference.com/register/league.cgi?id=3d6041f6'
r = requests.get(bref)
soup = BeautifulSoup(r.content, "html.parser")

st.title(":blue[LI]:red[DOM] Temporada 2024-2025 :flag-do::baseball:")
st.header("Estadísticas por Equipo")
st.subheader("Tabla de Posiciones")


cmap_sum_revert = matplotlib.colors.LinearSegmentedColormap.from_list("", ['#f81707', 'white', 'blue'])
cmap_sum = matplotlib.colors.LinearSegmentedColormap.from_list("", ['blue', 'white', '#f81707'])
##aqui ponemos las estadisticas basicas
if r.status_code == 200:
  standing = pd.DataFrame(pd.read_html([StringIO(soup.extract()) for soup in soup.find_all(string=lambda text: isinstance(text, Comment)) if 'id="div_standings_pitching"' in soup][0])[0])
  standing['J'] = standing['W']+standing['L']
  standing = standing[['Tm','J','W','L','W-L%','GB']]
  standing = standing.rename(columns={'Tm':'Equipo','W':'G','L':'P','W-L%':'Pct%','GB':'Dif'})
  formatted_standing = standing.style.format({"Pct%": "{:.3f}".format})

  formatted_standing = formatted_standing.background_gradient(subset=['Pct%'], cmap=cmap_sum,vmin=.222,vmax=.700)
  st.dataframe(formatted_standing, width=2000, hide_index=True)



  st.subheader("Estadísticas de Pitcheo")

  def FIP_Constant(stats):
    lgERA = stats.loc[stats['Tm']=='League Totals',['ERA']].values[0]
    lgHR = stats.loc[stats['Tm']=='League Totals',['HR']].values[0]
    lgBB = stats.loc[stats['Tm']=='League Totals',['BB']].values[0]
    lgHBP = stats.loc[stats['Tm']=='League Totals',['HBP']].values[0]
    lgK = stats.loc[stats['Tm']=='League Totals',['SO']].values[0]
    lgIP = stats.loc[stats['Tm']=='League Totals',['IP']].values[0]

    FIPc = "%.2f" % (lgERA - (((13*lgHR)+(3*(lgBB+lgHBP))-(2*lgK))/lgIP))
    return FIPc


  pitching_stats = pd.DataFrame(pd.read_html([StringIO(soup.extract()) for soup in soup.find_all(string=lambda text: isinstance(text, Comment)) if 'id="div_league_pitching"' in soup][0])[0])  
  FIPc = FIP_Constant(pitching_stats)
  st.markdown("Constante FIP: **"  + FIPc + "**")

  #FIP Formula
  #FIP = ((13*HR)+(3*(BB+HBP))-(2*K))/IP + constant
  pitching_stats['FIP'] = (((13*pitching_stats['HR'])+(3*(pitching_stats['BB']+pitching_stats['HBP']))-(2*pitching_stats['SO']))/pitching_stats['IP']) + float(FIPc)
  pitching_stats['K%'] = pitching_stats['SO']/pitching_stats['BF']
  pitching_stats['BB%'] = pitching_stats['BB']/pitching_stats['BF']
  pitching_stats = pitching_stats.rename(columns={'Tm':'Equipo'})
  pitching_stats = pitching_stats.drop(['Aff','PAge','W','L','W-L%','G','GS','GF','CG','SHO','H','R','ER','IBB','WP','BK','R/G','H9','SO/W','SV'], axis=1)
  pitching_stats = pitching_stats[:-1]
  pitching_stats = pitching_stats[['Equipo','IP','BF','ERA','FIP','RA9','SO9','BB9','HR9','WHIP','BB%','K%']]
  mapper =  {'ERA': '{0:.2f}',
           'RA9': '{0:.2f}',
           'WHIP': '{0:.2f}',
           'BB%': '{0:.2f}%',
           'K%': '{0:.2f}%',
           'IP': '{0:.1f}',
           'SO9': '{0:.1f}',
           'BB9': '{0:.1f}',
           'HR9': '{0:.1f}',
           'FIP': '{0:.2f}'}
  
  formatted_pitching_stats = pitching_stats.style.format(mapper).background_gradient(subset=['ERA'], cmap=cmap_sum_revert,vmin=2.71,vmax=4.81)
  formatted_pitching_stats = formatted_pitching_stats.background_gradient(subset=['FIP'], cmap=cmap_sum_revert,vmin=2.92,vmax=4.35)

  st.dataframe(formatted_pitching_stats, width=2000, hide_index=True)


  offensive_stats = pd.DataFrame(pd.read_html([StringIO(soup.extract()) for soup in soup.find_all(string=lambda text: isinstance(text, Comment)) if 'id="div_league_batting"' in soup][0])[0])
  offensive_stats['K%'] = offensive_stats['SO']/offensive_stats['PA']
  offensive_stats['BB%'] = offensive_stats['BB']/offensive_stats['PA']
  offensive_stats = offensive_stats.rename(columns={'Tm':'Equipo','R/G':'C/J'})
  offensive_stats = offensive_stats.drop(['Aff','BatAge','TB','GDP','HBP','SH','SF','IBB','SB','CS','G','AB','H','2B','3B','BB','SO','OPS'], axis=1)
  offensive_stats = offensive_stats[:-1]
  offensive_stats = offensive_stats[['Equipo','C/J','PA','HR','R','RBI','BB%','K%','BA','OBP','SLG']]
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
  
  
 
  