import requests
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
import sqlite3 as sql3
import matplotlib.pyplot as plt
import seaborn as sns

#WEB SCRAPPING 

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
#header for all browsers
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

html_data = requests.get(url, time.sleep(10), headers=headers).text
soup = bs(html_data, "html.parser")
tablas = soup.find_all('table')
t_revenue = tablas[1]
t_body = t_revenue.find('tbody')

date = []
sales = []

for row in t_body.find_all('tr'):
    datas_row = []  # Lista para almacenar los datos de esta fila
    for cell in row.find_all('td'):
        data = cell.get_text()
        datas_row.append(data)
    # Agrega los datos de la fila a las listas existentes
    if len(datas_row) >= 2:  # Verifica que haya al menos dos elementos en la fila
        date.append(datas_row[0])
        sales.append(datas_row[1])

sales = [data.replace(',', '').replace('$', '') for data in sales]

tesla_quarterly = pd.DataFrame({'Quarter date': date, 'Incomes': sales})
tesla_quarterly.head()

tesla_quarterly = pd.DataFrame({'Quarter date': date, 'Incomes': sales})

#SQL DATA

conn = sql3.connect('Tesla_sales.db')
#Conecta a la base de datos SQLite o la crea si no existe

# tesla_quarterly.to_sql('quarterly_income', conn, if_exists='replace', index=False)
# #Convierte mi pd.dataframe en tabla SQL

cursor = conn.cursor()
# cursor.execute("""CREATE TABLE income (date, sales)""")

tsl_tu = list(tesla_quarterly.to_records(index = False))
cursor.executemany("INSERT INTO income VALUES (?,?)", tsl_tu)
conn.commit()

for fila in cursor.execute("SELECT * FROM income"):
    print(fila)


#GRAPHICS


fig, axis = plt.subplots(figsize = (8, 4))

tesla_quarterly = tesla_quarterly[tesla_quarterly['Incomes'] != '']
tesla_quarterly['Incomes'] = tesla_quarterly['Incomes'].astype(int)
tesla_quarterly["Quarter date"] = pd.to_datetime(tesla_quarterly["Quarter date"])
sns.lineplot(data = tesla_quarterly, x = "Quarter date", y = "Incomes", color='red')

plt.tight_layout()

plt.show()



fig, axis = plt.subplots(figsize = (8, 4))

tesla_quarterly["Quarter date"] = pd.to_datetime(tesla_quarterly["Quarter date"])
tesla_quarter_year = tesla_quarterly.groupby(tesla_quarterly["Quarter date"].dt.year).sum().reset_index()
sns.barplot(data = tesla_quarter_year[tesla_quarter_year["Quarter date"] < 2023], x = "Quarter date", y = "Incomes")

plt.tight_layout()

plt.show()



fig, axis = plt.subplots(figsize = (8, 4))

tesla_monthly = tesla_quarterly.groupby(tesla_quarterly["Quarter date"].dt.month).sum().reset_index()
sns.barplot(data = tesla_monthly, x = "Quarter date", y = "Incomes")

plt.tight_layout()

plt.show()