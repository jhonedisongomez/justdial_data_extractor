import newspaper
from newspaper import Article
import csv, os
from bs4 import BeautifulSoup
import urllib
import requests
import pandas as pd
import re


newspaper_base_url = 'https://www.justdial.com/'
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

city_name = 'Ahmedabad'
keyword = 'hello'

cat_page_url = newspaper_base_url + city_name
html_markup = requests.get(cat_page_url, headers=headers)
print (html_markup.status_code)
page_soup = BeautifulSoup(html_markup.content, "lxml")


links = page_soup.find("section", {"class" : "container mid-section"}).find_all("figcaption", {"class" : "figure-text pl-15"})

def check_url(link):
    if "www.justdial.com" in link:
        return link
    else:
        return newspaper_base_url + link

output_file = "./output.csv"
if not os.path.exists(output_file):
    open(output_file, 'w').close() 


def gen_cat_list(cat_page_url_bycity):

    html_markup = requests.get(cat_page_url_bycity, headers=headers)
    page_soup = BeautifulSoup(html_markup.content, "lxml")
    filter_links = page_soup.find("ul", {"class" : "mm-listview"}).find_all("a")
    
    current_urls = []
    for flink in filter_links:
        current_urls.append(check_url(flink.get('href')))
        df = pd.DataFrame(current_urls)
        df.to_csv(output_file, index=False, header=False)
    print ('cat generated : {}'.format(city_name))
    

for link in links:
    cat_page_url_bycity = check_url(link.a['href']) + '/AllCategory'
    gen_cat_list(cat_page_url_bycity)
    break
    

with open(output_file, 'r') as f:
        url = f.readlines()
        for u in url:
            # print (u)
            html_markup = requests.get(u, headers=headers)
            # print (html_markup.status_code)
            page_soup = BeautifulSoup(html_markup.content, "lxml")
            contents = page_soup.find("ul", {"class" : "rsl col-md-12 padding0"}).find_all("li", {"class" : "cntanr"})
            
            for cont in contents:
                flag = True
                try:
                    title = cont.find("a", {"class" : "nlogo lazy srtbyPic" }).get('title')
                    rating = cont.find("span", {"class" : "exrt_count" }).get_text()
                    votes = cont.find("span", {"class" : "rt_count lng_vote" }).get_text().strip(' \t\n\r')[0:5:1].strip()

                    # enter into the page
                    single_url = cont.find("a", {"class" : "nlogo lazy srtbyPic" }).get('href')
                    html_markupx = requests.get(single_url, headers=headers)
                    page_soup = BeautifulSoup(html_markupx.content, "lxml")
                    cc = page_soup.find("div", {"class" : "col-sm-4 col-xs-12 padding0 leftdt"})
                    
                    contact = cc.find("div", {"class" : "telCntct cmawht"}).get_text()
                    address = cc.find("span", {"class" : "lng_add"}).get_text()
                    website = cc.find("span", {"class" : "mreinfp comp-text"}).find('a').find_next('a').get_text()

                except Exception as e:
                    pass
                    flag = False
                
                if flag is True:
                    print (city_name, title, rating, votes, contact, address, website)
