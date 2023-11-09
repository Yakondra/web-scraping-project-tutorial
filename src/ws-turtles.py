import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


option = webdriver.ChromeOptions()
option.add_argument("--headless")

driver = webdriver.Chrome(options=option)
driver.get('https://www.scrapethissite.com/pages/frames/')
time.sleep(10)

driver.switch_to.frame('iframe')
tortus = driver.find_elements(By.CLASS_NAME, 'btn')

tortu_names = [] 
tortu_descriptions = []

# tortu_names = [ts.text for ts in driver.find_elements(By.CLASS_NAME, "family-name")]
# tortu_names
# driver.find_element(By.CLASS_NAME, 'btn').click()
# time.sleep(5)

#No funciona Carlos, me quiero m00rir 

info = [ds.get_attribute('href') for ds in tortus]

for inf in info:
    
    driver_tortu = webdriver.Chrome(options=option)
    driver_tortu.get(inf)
    
    tortu_names.append(driver_tortu.find_element(By.CLASS_NAME, 'family-name').text)
    tortu_descriptions.append(driver_tortu.find_element(By.CLASS_NAME, 'lead').text)
    
    driver_tortu.close()
    
driver.quit()
    
#Import re para que me ayude a extraer datos (hago expresion regular)

exg_ = r'\d+'

#r'\d+' para buscar num int, r'\d+\.\d+' para num float
#r'-?\d+\.\d+' para num negativo

year_tortu = []

for descpt in tortu_descriptions:
    num = re.findall(exg_, descpt)
    year_tortu.extend(num)
    
year_tortu = [int(numero) for numero in year_tortu]

tabla_tortu = pd.DataFrame({'Nombre científico': tortu_names, 'Año descubrimiento': year_tortu})
tabla_tortu.set_index(pd.Index(range(1, len(tortu_names) + 1)), inplace=True)

tabla_tortu

#Encontré otra manera, espero que sirva xD