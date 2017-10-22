# -*- coding: utf-8 -*-
from io import BytesIO
import xlsxwriter
from django.utils.translation import ugettext
from celery import shared_task

#from newspaper import Article
import requests

from .models import CrawelIssue
import csv, os
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
    fileName = city_name + "_" + str(now.day) + "_" +  str(now.month) + "_" + str(now.year) + "_" + str(now.hour) + "_" + str(now.minute) + "_"+str(now.second) + ".xls" 
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=' + fileName

    try:
        
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet_s = workbook.add_worksheet()
        #fields = ['user','keyword','city_name','instance_index','title', 'rating','votes', 'contact', 'address', 'website']
        #out = csv.DictWriter(response, fieldnames=fields)
        #out.writeheader()

        worksheet_s.write(0, 0, ugettext("user"))
        worksheet_s.write(0, 1, ugettext("keyword"))
        worksheet_s.write(0, 2, ugettext("city_name"))
        worksheet_s.write(0, 3, ugettext("instance_index"))
        worksheet_s.write(0, 4, ugettext("title"))
        worksheet_s.write(0, 5, ugettext("rating"))
        worksheet_s.write(0, 6, ugettext("votes"))
        worksheet_s.write(0, 7, ugettext("contact"))
        worksheet_s.write(0, 8, ugettext("address"))
        worksheet_s.write(0, 9, ugettext("website"))

        print (city_name, keyword, numof_pages)
        print ('requested by user id: {}'.format(user))

        driver = webdriver.Chrome("G:/freelance/justdial_data_extractor/.env/selenium/webdriver/chromedriver.exe")
        driver2 = webdriver.Chrome("G:/freelance/justdial_data_extractor/.env/selenium/webdriver/chromedriver.exe")   
        city_name, keyword, numof_pages, user = data[0], data[1], int(data[2]), data[3]
        example = ""
        html_markup = {}
        url = ""
        print (city_name, keyword, numof_pages)
        print ('requested by user id: {}'.format(user))

        instance_index = 0
        pages_set = 0
        y = 1
        for page in range(numof_pages):
        
            pages_set = pages_set + 1
            page = 'https://www.justdial.com/' + city_name + '/' + keyword + '/page-'+ str(pages_set)
            print(page)
            driver.get(page)
            elem = driver.find_element_by_tag_name("body")

            no_of_pagedowns = 1

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

                """out.writerow({ 'user':user,
                                  'keyword':keyword,
                                  'city_name':city_name,
                                  'instance_index':instance_index,
                                  'title':title,
                                  'rating':rating,
                                  'votes':votes,
                                  'contact':contacts,
                                  'address':address,
                                  'website':website})"""

                worksheet_s.write(y+1, 0, str(user))
                worksheet_s.write(y+1, 1, str(keyword))
                worksheet_s.write(y+1, 2, str(city_name))
                worksheet_s.write(y+1, 3, str(instance_index))
                worksheet_s.write(y+1, 4, str(title))
                worksheet_s.write(y+1, 5, str(rating))
                worksheet_s.write(y+1, 6, str(votes))
                worksheet_s.write(y+1, 7, str(contacts))
                worksheet_s.write(y+1, 8, str(address))
                worksheet_s.write(y+1, 9, str(website))
                y +=1

                print ( 'No: {}, Saving data to file.'.format(instance_index))
                instance_index += 1 

        print('I am here')      
        workbook.close()
        print ('close')
        xlsx_data = output.getvalue()
        print('hello')
        response.write(xlsx_data)
        print('hi')
    except Exception as e:
        print(e) 

    
    return response