from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import urllib
from tqdm import tqdm
import uuid
import time

web = 'https://unsplash.com/s/photos/empty-room'
path = '/Users/DELL/Downloads/chromedriver.exe'  

driver_service = Service(executable_path=path)
driver = webdriver.Chrome(service=driver_service)

uids =[]
image_urls = []
titles = []
        
#code for 1 page using load more option 
driver.get(web)

driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div[4]/div/div[3]/div[1]/button').click()  #for loadmore clicking 

for i in tqdm(range(1,1001)): #for reloading of the page cause execute scripts scrolls to a certain height, here 101 is a guess 
    
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #for scrolling till max height of page to do all scraping once 
        
containers = driver.find_elements(by='xpath', value='//figure[contains(@itemprop,"image")]')

for container in tqdm(containers):
    
    div_url = container.find_element(By.CLASS_NAME, 'MorZF')
    img_tag_url = div_url.find_element(By.TAG_NAME, 'img')
    href = img_tag_url.get_attribute('srcset')
    listt = href.split(',')
    url = listt[0].split('?')[0]
    image_urls.append(url)
    
    #code for collecting uuids
    u=uuid.uuid1()
    uids.append(u)
    
    #code for collecting titles
    div_title = container.find_element(By.CLASS_NAME, 'MorZF')
    img_tag_title = div_title.find_element(By.TAG_NAME, 'img')
    alt = img_tag_title.get_attribute('alt')
    titles.append(alt)

my_dict = {'uids':uids ,'image_url': image_urls,'title': titles }
df_headlines = pd.DataFrame(my_dict)
df_headlines.to_csv('empty_bedroom_images7.csv')

driver.quit()
