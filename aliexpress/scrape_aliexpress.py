import pandas as pd
import mysql.connector
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy import Selector
from selenium.webdriver.chrome.options import Options


chrome_options = Options()  
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
driver.maximize_window()

def scrape_product(url,category):
    list_of_dict = list()
    for page_num in range(1,3):
        while(1):
            try:
                print('Page Num: ', page_num)
                url = url + '&page={}'
                url = url.format(page_num)
                driver.get(url)   
                time.sleep(1)
                for i in range(0,9):
                    html = driver.find_element(By.CSS_SELECTOR,'a._3t7zg._2f4Ho')
                    html.send_keys(Keys.PAGE_DOWN)
                    time.sleep(2)

                res = Selector(text=driver.page_source)
                products_page_links = res.css('div.JIIxO a._3t7zg._2f4Ho::attr(href)').getall()
                product_number = 1
                for link in products_page_links:
                    try:
                        print('Product Number',product_number)
                        product_number += 1
                        temp = dict()
                        link = 'https:'+link
                        driver.get(link)
                        time.sleep(1)
                        res1 = Selector(text=driver.page_source)
                        name = res1.css('h1.product-title-text::text').get()
                        price = res1.css('span.product-price-value::text').get()
                        if not price:
                            price = res1.css('span.uniform-banner-box-price::text').get()
                        images = res1.css('div.sku-property-image img::attr(src)').getall()
                        if images:
                            images = ','.join(images)
                        sizes = res1.css('div.sku-property-text span::text').getall()
                        if sizes:
                            sizes = ','.join(sizes)
                        else:
                            sizes = None
                        color = res1.css('span.sku-title-value::text').get()
                
                        temp['name'] = name
                        temp['price'] = price
                        temp['images'] = images
                        temp['size'] = sizes
                        temp['color'] = color
                        temp['category'] = category

                        print('Temp: ', temp)

                        list_of_dict.append(temp)
                    except:
                        driver.refresh()
                        time.sleep(1)
                        res1 = Selector(text=driver.page_source)
                        name = res1.css('h1.product-title-text::text').get()
                        price = res1.css('span.product-price-value::text').get()
                        if not price:
                            price = res1.css('span.uniform-banner-box-price::text').get()
                        images = res1.css('div.sku-property-image img::attr(src)').getall()
                        if images:
                            images = ','.join(images)
                        sizes = res1.css('div.sku-property-text span::text').getall()
                        if sizes:
                            sizes = ','.join(sizes)
                        else:
                            sizes = None
                        color = res1.css('span.sku-title-value::text').get()
                
                        temp['name'] = name
                        temp['price'] = price
                        temp['images'] = images
                        temp['size'] = sizes
                        temp['color'] = color
                        temp['category'] = category

                        print('Temp: ', temp)

                        list_of_dict.append(temp)

                break
            except:
                driver.refresh()
                
    return list_of_dict

### For Girls Clothing ###
def girls_clothing_category():
    url = 'https://www.aliexpress.com/category/100003199/girls-clothing.html?trafficChannel=main&catName=girls-clothing&CatId=100003199&ltype=wholesale&SortType=default'
    girls_list = scrape_product(url,'girls_clothing')
    girls_df = pd.DataFrame(girls_list)
    girls_df.to_csv('girls.csv',index=False)

### For Boys Clothing ###
def boys_clothing_category():
    url = 'https://www.aliexpress.com/category/100003186/boys-clothing.html?trafficChannel=main&catName=boys-clothing&CatId=100003186&ltype=wholesale&SortType=default'
    boys_list = scrape_product(url,'boys_clothing')
    boys_df = pd.DataFrame(boys_list)
    boys_df.to_csv('boys.csv',index=False)

### For Kids Shoes ###
def kids_shoes_category():
    url = 'https://www.aliexpress.com/category/32212/children-shoes.html?trafficChannel=main&catName=children-shoes&CatId=32212&ltype=wholesale&SortType=default'
    kids_shoes_list = scrape_product(url,'kids_shoes')
    kids_shoes_df = pd.DataFrame(kids_shoes_list)
    kids_shoes_df.to_csv('kids_shoes.csv',index=False)

### For Kids Toys ###
def kids_toys_category():
    url = 'https://www.aliexpress.com/category/26/toys-hobbies.html?trafficChannel=main&catName=toys-hobbies&CatId=26&ltype=wholesale&SortType=default'
    kids_toys_list = scrape_product(url,'kids_toys')
    kids_toys_df = pd.DataFrame(kids_toys_list)
    kids_toys_df.to_csv('kids_toys.csv',index=False)


def create_mysql_connection():
    mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'aliexpress')
    
    return mydb

def create_mysql_table(mycursor):
    mycursor.execute("CREATE TABLE products (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name TEXT, price TEXT, images TEXT, size TEXT, color TEXT, category TEXT)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci") 

def data_read_and_cleaning():
    girls = pd.read_csv('girls.csv')
    boys = pd.read_csv('boys.csv')
    kids_shoes = pd.read_csv('kids_shoes.csv')
    kids_toys = pd.read_csv('kids_toys.csv')

    data = pd.concat([girls,boys,kids_shoes,kids_toys])
    data = girls
    data['price'] = data['price'].fillna('0')
    data['images'] = data['images'].replace('[]','')
    data['size'] = data['size'].fillna('0')
    data['color'] = data['size'].fillna('0')
    
    return data

def insert_records_into_db(data,mydb,mycursor):
    for i,row in data.iterrows():
        sql = "INSERT INTO products(name,price,images,size,color,category) VALUES(%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql, tuple(row))
        mydb.commit()

def main():
    
    ### Scrape Products from Category Wise ###
    girls_clothing_category()
    boys_clothing_category()
    kids_shoes_category()
    kids_toys_category()
    
    ### Connection with MySQL Database
    mydb = create_mysql_connection()
    mycursor = mydb.cursor()
    ### Create MySQL Database Table
    create_mysql_table(mycursor)
    ### Read and clean pandas dataframe
    data = data_read_and_cleaning()
    ### Insert Records into Products MySQL Table
    insert_records_into_db(data,mydb,mycursor)
    print("Records inserted")
    

if __name__ == '__main__':
    main()
