##pip install prettytable
import os
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable


url = 'https://estadisticas.lidom.com/'
respuesta = requests.get(url)
if respuesta.status_code == 200:
  total_teams = 6
  soup = BeautifulSoup(respuesta.text, 'html.parser')
  ##print(x)
  W = soup.find_all('table')[1].find_all('tr')[1].find_all('td')[1].get_text().strip() 
  L = soup.find_all('table')[1].find_all('tr')[1].find_all('td')[2].get_text().strip() 
  PCT = soup.find_all('table')[1].find_all('tr')[1].find_all('td')[3].get_text().strip() 
  
  
headers = ("Equipo", "W - L", "PCT")
standing = PrettyTable(headers)

if respuesta.status_code == 200:
  total_teams = 6
  soup = BeautifulSoup(respuesta.text, 'html.parser')

  for x in range(total_teams):
    x += 1
    ##print(x)
    equipo = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[0].find_all('a')[0].get_text().strip() ##nombre del equipo
    w = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[2].get_text().strip() 
    l = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[3].get_text().strip() 
    wl = w + " - " + l
    pct = soup.find_all('table')[1].find_all('tr')[x].find_all('td')[4].get_text().strip() 
  
  
    standing.add_row([equipo, wl, pct])


standing.padding_width = 5
standing.border = True
standing.sortby = 'PCT'

standing.align['Equipo'] = 'l'
standing.align['PCT'] = 'r'
standing.reversesort = True
print(standing)