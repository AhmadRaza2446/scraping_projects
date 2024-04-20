import re
import time
import csv
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from scrapy import Selector
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
cities = pd.read_csv('German Cities top 200 .csv', encoding= 'unicode_escape')

list_of_dict = list()
for city in cities['cities'][19:20]:
    
    driver.get('https://www.google.com/search?q={}+zip+codes'.format(city))
    time.sleep(5)
    res = Selector(text=driver.page_source)
    zipcodes = res.css('div.bVj5Zb.FozYP::text').getall()[5:]
    
    if not zipcodes:
        zipcodes = res.css('#main > div:nth-child(5) > div > div > a > div > div > span > div::text').getall()[5:]
    print(zipcodes)
    names = list()
    addresses = list()
    count = 1
    for zipcode in zipcodes:
        if count < 350:
            try:
                driver.get('https://www.google.com/search?q={}+ restaurants {}'.format(zipcode,city))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                '#Odp5De > div > div > div.tJicRe > div:nth-child(3) > div > div:nth-child(1) > div > div.F7IIOc.xaNsfc > div')))
                time.sleep(5)
                driver.find_element_by_css_selector('#Odp5De > div > div > div.tJicRe > div:nth-child(3) > div > div:nth-child(1) > div > div.F7IIOc.xaNsfc > div').click()
                time.sleep(2)
                driver.find_element_by_css_selector('#filter_1 > div:nth-child(3) > span:nth-child(1) > span:nth-child(1)').click()
                time.sleep(2)



                while(1):
                    res = Selector(text=driver.page_source)
                    restaurant_names = res.css('div.rllt__details div.dbg0pd.eDIkBe span.OSrXXb::text').getall()
                    restaurant_addresses = res.css('a.vwVdIc.wzN8Ac.rllt__link.a-no-hover-decoration > div > div > div:nth-child(3)::text').getall()
                    # restaurant_urls = res.css('a.hfpxzc::attr(href)').getall()
                    # restaurant_names = res.css('a.hfpxzc::attr(aria-label)').getall()
#                     print('Names: ',restaurant_names)
#                     print('Addresses: ',restaurant_addresses)

                    names.extend(restaurant_names)
                    addresses.extend(restaurant_addresses)


                    next_page = res.css('#pnnext::attr(href)').get()

                    if next_page:

                        next_page = 'https://www.google.com' + next_page
                        driver.get(next_page)
                    else:
                        break

                print('RESTAURANT NAMES: ', names)
                print('RESTAURANT ADDRESSES: ', addresses)


                
            except:
                pass
        else:
            break
#             driver.find_element_by_css_selector('button.B7V4Ld').click()
    count = 0
    for name,address in zip(names,addresses):
        print('Count: ', count)
        count += 1
        try:
            print('Name: ',name)
            print('address: ',address)
            driver.get('https://www.google.com/maps/')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Odp5De > div > div > div.tJicRe > div:nth-child(3) > div > div:nth-child(1) > div > div.F7IIOc.xaNsfc > div')))
    
            time.sleep(3)
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "(//input[@class='tactile-searchbox-input'])[1]"))).send_keys("{} {}".format(name,address))
            time.sleep(5)
            driver.find_element_by_css_selector("div.DgCNMb").click()
#                 driver.find_element_by_css_selector("#searchbox-searchbutton").click()

            temp=dict()
            time.sleep(10)
            res1 = Selector(text=driver.page_source)
            address = res1.css('div.Io6YTe.fontBodyMedium::text').get()
            address1 = address.split(',')
#                 print('Address1: ', address1)
            if len(address1) > 3:
                address1 = address1[1:]

            zipcode = address1[1].strip().split(" ")[0]
        #     zipcode = address1[1].split(" ")[0]

            town = address1[1].strip().split(" ")
#                 if len(town) == 2:
#                     town = town[0]
#                 else:
            town = " ".join(town[1:])
            street = address1[0]
            rating = res1.css('div.F7nice > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)::text').get()
            total_reviews = res1.css('.F7nice button.DkEaL::text').get()


#                         print('Name: ', name)
#                         print('Street: ', street)
#                         print('Zip Code: ', zipcode)
#                         print('Town: ', town)
#                         print('Rating: ', rating)
#                         print('Total Reviews: ', total_reviews)

            temp = dict()
            temp['name'] = name
            temp['street'] = street
            temp['zipcode'] = zipcode
            temp['town'] = town
            temp['rating'] = rating
            temp['total_reviews'] = total_reviews
            list_of_dict.append(temp)
        except:
            try:
#                             print('Name: ',name)
#                             print('address: ',address)
                driver.get('https://www.google.com/maps/')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Odp5De > div > div > div.tJicRe > div:nth-child(3) > div > div:nth-child(1) > div > div.F7IIOc.xaNsfc > div')))
    
                time.sleep(3)
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "(//input[@class='tactile-searchbox-input'])[1]"))).send_keys("{} {}".format(name,address))
                time.sleep(5)
                driver.find_element_by_css_selector("div.DgCNMb").click()
#                     driver.find_element_by_css_selector("#searchbox-searchbutton").click()
                temp=dict()
                time.sleep(10)
                restaurant_url = res1.css('a.hfpxzc::attr(href)').get()
#                             print(restaurant_url)
                driver.get(restaurant_url)
                time.sleep(2)
                res1 = Selector(text=driver.page_source)
                address = res1.css('div.Io6YTe.fontBodyMedium::text').get()
                address1 = address.split(',')
#                             print('Address1: ', address1)
                if len(address1) > 3:
                    address1 = address1[1:]

                zipcode = address1[1].strip().split(" ")[0]
            #     zipcode = address1[1].split(" ")[0]

                town = address1[1].strip().split(" ")
#                 if len(town) == 2:
#                     town = town[0]
#                 else:
                town = " ".join(town[1:])
                street = address1[0]
                rating = res1.css('div.F7nice > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)::text').get()
                total_reviews = res1.css('.F7nice button.DkEaL::text').get()


#                             print('Name: ', name)
#                             print('Street: ', street)
#                             print('Zip Code: ', zipcode)
#                             print('Town: ', town)
#                             print('Rating: ', rating)
#                             print('Total Reviews: ', total_reviews)

                temp = dict()
                temp['name'] = name
                temp['street'] = street
                temp['zipcode'] = zipcode
                temp['town'] = town
                temp['rating'] = rating
                temp['total_reviews'] = total_reviews
                list_of_dict.append(temp)

            except:
                try:
#                                 print('Name: ',name)
#                                 print('address: ',address)

#                     address = address.strip().split(" ")[0]
#                     print('New address: ', address)
                    driver.get('https://www.google.com/maps/')
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Odp5De > div > div > div.tJicRe > div:nth-child(3) > div > div:nth-child(1) > div > div.F7IIOc.xaNsfc > div')))
    
                    time.sleep(3)
                    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "(//input[@class='tactile-searchbox-input'])[1]"))).send_keys("{}".format(name))
                    time.sleep(5)
                    driver.find_element_by_css_selector("div.DgCNMb").click()

                    temp=dict()
                    time.sleep(10)
                    res1 = Selector(text=driver.page_source)
                    address = res1.css('div.Io6YTe.fontBodyMedium::text').get()
                    address1 = address.split(',')
#                                 print('Address1: ', address1)
                    if len(address1) > 3:
                        address1 = address1[1:]

                    zipcode = address1[1].strip().split(" ")[0]
            #     zipcode = address1[1].split(" ")[0]

                    town = address1[1].strip().split(" ")
    #                 if len(town) == 2:
    #                     town = town[0]
    #                 else:
                    town = " ".join(town[1:])
                    street = address1[0]
                    rating = res1.css('div.F7nice > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)::text').get()
                    total_reviews = res1.css('.F7nice button.DkEaL::text').get()


#                                 print('Name: ', name)
#                                 print('Street: ', street)
#                                 print('Zip Code: ', zipcode)
#                                 print('Town: ', town)
#                                 print('Rating: ', rating)
#                                 print('Total Reviews: ', total_reviews)

                    temp = dict()
                    temp['name'] = name
                    temp['street'] = street
                    temp['zipcode'] = zipcode
                    temp['town'] = town
                    temp['rating'] = rating
                    temp['total_reviews'] = total_reviews
                    list_of_dict.append(temp)
                except:
                    try:
                        time.sleep(3)
                        restaurant_url = res1.css('a.hfpxzc::attr(href)').get()
#                                     print(restaurant_url)
                        driver.get(restaurant_url)
                        time.sleep(5)
                        temp=dict()

                        res1 = Selector(text=driver.page_source)
                        address = res1.css('div.Io6YTe.fontBodyMedium::text').get()
                        try:
                            address1 = address.split(',')
                        except:
                            address = res1.css('span.DkEaL::text').get()
                            address1 = address.split(',')
#                                     print('Address1: ', address1)
                        if len(address1) > 3:
                            address1 = address1[1:]

                        zipcode = address1[1].strip().split(" ")[0]
                    #     zipcode = address1[1].split(" ")[0]

                        town = address1[1].strip().split(" ")
        #                 if len(town) == 2:
        #                     town = town[0]
        #                 else:
                        town = " ".join(town[1:])
                        street = address1[0]
                        rating = res1.css('div.F7nice > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)::text').get()
                        total_reviews = res1.css('.F7nice button.DkEaL::text').get()


#                                     print('Name: ', name)
#                                     print('Street: ', street)
#                                     print('Zip Code: ', zipcode)
#                                     print('Town: ', town)
#                                     print('Rating: ', rating)
#                                     print('Total Reviews: ', total_reviews)

                        temp = dict()
                        temp['name'] = name
                        temp['street'] = street
                        temp['zipcode'] = zipcode
                        temp['town'] = town
                        temp['rating'] = rating
                        temp['total_reviews'] = total_reviews
                        list_of_dict.append(temp)

                    except:
#                                     print('Name: ',name)
#                                     print('address: ',address)
                        driver.get('https://www.google.com/maps/')
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Odp5De > div > div > div.tJicRe > div:nth-child(3) > div > div:nth-child(1) > div > div.F7IIOc.xaNsfc > div')))
    
                        time.sleep(3)
                        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "(//input[@class='tactile-searchbox-input'])[1]"))).send_keys("{} {}".format(name,city))
                        time.sleep(5)
                        driver.find_element_by_css_selector("div.DgCNMb").click()
    #                     driver.find_element_by_css_selector("#searchbox-searchbutton").click()
                        temp=dict()
                        time.sleep(10)
#                             restaurant_url = res1.css('a.hfpxzc::attr(href)').get()
#                             print(restaurant_url)
#                             driver.get(restaurant_url)
#                             time.sleep(2)
                        res1 = Selector(text=driver.page_source)
                        address = res1.css('div.Io6YTe.fontBodyMedium::text').get()
                        address1 = address.split(',')
#                                     print('Address1: ', address1)
                        if len(address1) > 3:
                            address1 = address1[1:]

                        zipcode = address1[1].strip().split(" ")[0]
                    #     zipcode = address1[1].split(" ")[0]

                        town = address1[1].strip().split(" ")
        #                 if len(town) == 2:
        #                     town = town[0]
        #                 else:
                        town = " ".join(town[1:])
                        street = address1[0]
                        rating = res1.css('div.F7nice > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)::text').get()
                        total_reviews = res1.css('.F7nice button.DkEaL::text').get()


                        print('Name: ', name)
                        print('Street: ', street)
                        print('Zip Code: ', zipcode)
                        print('Town: ', town)
                        print('Rating: ', rating)
                        print('Total Reviews: ', total_reviews)

                        temp = dict()
                        temp['name'] = name
                        temp['street'] = street
                        temp['zipcode'] = zipcode
                        temp['town'] = town
                        temp['rating'] = rating
                        temp['total_reviews'] = total_reviews
                        list_of_dict.append(temp)

    print('Temp: ',temp)
        