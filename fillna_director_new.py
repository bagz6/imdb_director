from re import search
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd


url = 'https://www.imdb.com'
data = pd.read_csv('d:/mediatropy/run_ulang.csv')

search_bar = ".//div[@class='sc-crrsfI iDhzRL searchform__inputContainer']/div/input"
search_bar2 = ".//*[@id='suggestion-search']"
type_text = ".//div[@class='react-autosuggest__container']/input"
list_click = ".//*[@id='main']/div/div[2]/table/tbody/tr[1]/td[2]/a"
cast = ".//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[1]/div/div[2]/ul/li[1]/a"
cast2 = ".//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/a[2]"
cast3 = 'a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link'
director = ".//*[@id='fullcredits_content']/table[1]/tbody/tr/td[1]/a"
director2 = ".//*[@id='fullcredits_content']/table[1]/tbody/tr[1]/td[1]/a"

ulang = []
director_name = []

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get(url)
driver.find_element(by=By.XPATH, value=search_bar).click()
text = driver.find_element(by=By.XPATH, value=type_text)
text.send_keys(data['title'][0])
text.send_keys(Keys.RETURN)
driver.find_element(by=By.XPATH, value=list_click).click()
driver.execute_script("window.scrollTo(0,500)")
driver.find_element(by=By.XPATH, value=cast).click()
u_url = driver.current_url
info = driver.find_element(by=By.XPATH, value=director)
director = {
    'title' : data['title'][0],
    'surl'  : u_url, 
    'director' : info.text
}
director_name.append(director)

df = pd.DataFrame(director_name)
print(df)

for x in range(1, len(data['title'])):
    driver.find_element(by=By.XPATH, value=search_bar2).click()
    text = driver.find_element(by=By.XPATH, value=type_text)
    text.send_keys(data['title'][x])
    text.send_keys(Keys.RETURN)
    try:
        driver.find_element(by=By.XPATH, value=list_click).click()
    except:
        continue
    driver.execute_script("window.scrollTo(0,500)")
    try:
        driver.find_element(by=By.XPATH, value=cast).click()
    except:
        continue
    u_url = driver.current_url
    try:
        info = driver.find_element(by=By.XPATH, value=director)
        director = {
            'title' : data['title'][x],
            'surl'  : u_url, 
            'director' : info.text
        }
        director_name.append(director)
    except:
        try:
            info = driver.find_element(by=By.XPATH, value=director2)
            director = {
            'title' : data['title'][x],
            'surl'  : u_url, 
            'director' : info.text
            }
            director_name.append(director)
        except:
            fail ={
                'title' : data['title'][x],
                'surl'  : u_url
            }
            ulang.append(fail)
            continue

    df = pd.DataFrame(director_name)
    print(df)
    df.to_csv('d:/mediatropy/fill_director_new_6.csv')

df1 = pd.DataFrame(ulang)
print(df1)
df1.to_csv('d:/mediatropy/not_found_director_2.csv')

