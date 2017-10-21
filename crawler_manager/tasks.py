from celery import shared_task

from newspaper import Article
from bs4 import BeautifulSoup
import requests

from .models import CrawelIssue
import csv, os
import pandas as pd
import re
from datetime import datetime
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

newspaper_base_url = 'https://www.justdial.com/'
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

def check_url(link):
    if "www.justdial.com" in link:
        return link
    else:
        return newspaper_base_url + link




@shared_task
def start_srabbing(data, request):
    
    city_name, keyword, numof_pages, user = data[0], data[1], int(data[2]), data[3]
    
    now = datetime.now()
    fileName = city_name + "_" + str(now.day) + "_" +  str(now.month) + "_" + str(now.year) + "_" + str(now.hour) + "_" + str(now.minute) + "_"+str(now.second) + ".csv" 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=' + fileName

    try:
        
        
        fields = ['user','keyword','city_name','instance_index','title', 'rating','votes', 'contact', 'address', 'website']
        out = csv.DictWriter(response, fieldnames=fields)
        out.writeheader()

        print (city_name, keyword, numof_pages)
        print ('requested by user id: {}'.format(user))

        driver = webdriver.Chrome('/home/desarrollador/Documentos/.projects/justdial_data_extractor/.env/selenium/webdriver/chromedriver')
        driver2 = webdriver.Chrome('/home/desarrollador/Documentos/.projects/justdial_data_extractor/.env/selenium/webdriver/chromedriver')   
        city_name, keyword, numof_pages, user = data[0], data[1], int(data[2]), data[3]
        example = ""
        html_markup = {}
        url = ""
        print (city_name, keyword, numof_pages)
        print ('requested by user id: {}'.format(user))

        instance_index = 0
        pages_set = 0

        for page in range(numof_pages):
        
            pages_set = pages_set + 1
            page = 'https://www.justdial.com/' + city_name + '/' + keyword + '/page-'+ str(pages_set)
            print(page)
            driver.get(page)
            elem = driver.find_element_by_tag_name("body")

            no_of_pagedowns = 100

            while no_of_pagedowns:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                no_of_pagedowns-=1

            isContact = False
            for i in driver.find_elements_by_class_name("cntanr"):

                title = i.find_element_by_class_name("srtbyPic").get_attribute("title")
                rating = i.find_element_by_class_name("exrt_count").get_attribute("innerHTML")
                votes = i.find_element_by_class_name("lng_vote").get_attribute("innerHTML").strip(' \t\n\r')[0:5:1].strip()
                single_url = i.find_element_by_class_name("rating_div").get_attribute("href")
                contacts = ""
                address = ""
                website = ""
                driver2.get(single_url)
                elem2 = driver2.find_element_by_tag_name("body")
                elem2.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                for contact in elem2.find_elements_by_class_name("leftdt"):
                    for tel in contact.find_elements_by_class_name("tel"):
                        contacts =  contacts + " " + tel.get_attribute("innerHTML")
                        contacts = contacts.replace("<b>","")
                        contacts = contacts.replace("</b>","")
                    print(contacts)
                    address = contact.find_element_by_class_name("lng_add").get_attribute("innerHTML")
                    websites = contact.find_elements_by_css_selector(".mreinfp.comp-text")
                    website = ""
                    for ix,get_website  in enumerate(websites):
                        if ix == 1:
                    
                            website = get_website.find_element_by_tag_name("a").get_attribute("href")

                """issue = CrawelIssue.objects.create(
                user = user,
                keyword = keyword, 
                city_name = city_name, 
                # crawel_number = crawel_number, 
                instance_index = instance_index, 
                title = title, 
                rating = rating, 
                votes = votes, 
                contact = contacts, 
                address = address, 
                website = website,
                )"""

                out.writerow({ 'user':user,
                                  'keyword':keyword,
                                  'city_name':city_name,
                                  'instance_index':instance_index,
                                  'title':title,
                                  'rating':rating,
                                  'votes':votes,
                                  'contact':contacts,
                                  'address':address,
                                  'website':website})


                print ( 'No: {}, Saving data to database.'.format(instance_index))
                instance_index += 1       
    
    except Exception as e:
        print(e) 


    return response