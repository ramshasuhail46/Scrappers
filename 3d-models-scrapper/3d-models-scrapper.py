from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from tqdm import tqdm
import uuid

models = {'aircraft': 66, 'animals':258,'architectural':97, 'street':18, 'electric':131, 'foods':52, 'furniture':315, 'cg':82, 'garden':53, 'hospital':22, 'human':197 , 'industial':24, 'kitchen':71, 'lamp':147, 'plant':100, 'sports':68, 'vehicle':181, 'watercraft':35, 'weapons':126}

web = 'https://www.cadnav.com/3d-models/'
path = 'C:/Users/ABC/Desktop/chromedriver-win64/chromedriver.exe'

driver_service = Service(executable_path=path)
driver = webdriver.Chrome(service=driver_service)

page_urls = []
uids =[]
image_urls = []
titles = []
descriptions = []
types =[]

def pages_links(model_to_be_scrapped, web,total_pages):
     for i in range(1,total_pages+1):
        li=web+model_to_be_scrapped+'/index-'+str(i)+'.html'
        page_urls.append(li)

def scrapper(page_urls):
    
    for i in range(1,len(page_urls)):
        
        driver.get(page_urls[i])
        containers = driver.find_elements(by='xpath', value='/html/body/main/section/div[2]/div')
    
        for container in containers:
            
            div_url = container.find_element(By.CLASS_NAME, 'entry-cat-dot')
            type = div_url.text
            types.append(type)
            
            u=uuid.uuid1()
            uids.append(u)

            div_title = container.find_element(By.CLASS_NAME, 'entry-title')
            title = div_title.text
            titles.append(title)

            div_description = container.find_element(By.CLASS_NAME, 'entry-meta')
            description = div_description.text
            descriptions.append(description)

            div_url = container.find_element(By.CLASS_NAME, 'entry-media.ratio.ratio-4x3')
            a = div_url.find_element(By.CLASS_NAME, 'media-img.lazy')
            href = a.get_attribute('href')
            image_urls.append(href)

for key in tqdm(models):

    uids.clear()
    titles.clear()
    types.clear()
    descriptions.clear()
    image_urls.clear()
    page_urls.clear()

    model_to_be_scrapped = key 
    total_pages = models[key]

    pages_links(model_to_be_scrapped, web, total_pages)
    scrapper(page_urls)
   
    my_dict = {'UUID':uids ,'Titles': titles,'Type': types, 'Description': descriptions, 'Urls': image_urls}
    df_headlines = pd.DataFrame(my_dict)
    df_headlines.to_csv('3D-models-'+model_to_be_scrapped+'.csv')


driver.quit()            
