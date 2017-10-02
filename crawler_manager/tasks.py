from celery import shared_task

from newspaper import Article
from bs4 import BeautifulSoup
import requests

from .models import CrawelIssue

newspaper_base_url = 'https://www.justdial.com/'
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

def check_url(link):
    if "www.justdial.com" in link:
        return link
    else:
        return newspaper_base_url + link




@shared_task
def start_srabbing(data):
    
    city_name, keyword, numof_pages = data[0], data[1], int(data[2])

    print (city_name)
    print (keyword)
    print (numof_pages)

    instance_index = 0
    for i in range(numof_pages):
        city_page_url = newspaper_base_url + city_name + '/' + keyword + '/' + 'page-' + str(i+1)
        
        html_markup = requests.get(check_url(city_page_url), headers=headers)
        print ('got page url {} with {}'.format(city_page_url, html_markup.status_code))

        page_soup = BeautifulSoup(html_markup.content, "lxml")
        contents = page_soup.find("ul", {"class" : "rsl col-md-12 padding0"}).find_all("li", {"class" : "cntanr"})
                
        for cont in contents:
            flag = True
            try:
                title = cont.find("a", {"class" : "nlogo lazy srtbyPic" }).get('title')
                try:
                    rating = cont.find("span", {"class" : "exrt_count" }).get_text()
                except Exception as e:
                    rating = ''
                    pass
                try:
                    votes = cont.find("span", {"class" : "rt_count lng_vote" }).get_text().strip(' \t\n\r')[0:5:1].strip()
                except Exception as e:
                    votes = ''
                    pass
                
                # enter into the page
                single_url = cont.find("a", {"class" : "nlogo lazy srtbyPic" }).get('href')
                html_markupx = requests.get(check_url(single_url), headers=headers)
                page_soup = BeautifulSoup(html_markupx.content, "lxml")
                cc = page_soup.find("div", {"class" : "col-sm-4 col-xs-12 padding0 leftdt"})
                
                contact = cc.find("div", {"class" : "telCntct cmawht"}).get_text() # compulsory field to scrab
                
                try:
                    address = cc.find("span", {"class" : "lng_add"}).get_text()
                except Exception as e:
                    address = ''
                    pass
                try:
                    website = cc.find("span", {"class" : "mreinfp comp-text"}).find('a').find_next('a').get_text()
                except Exception as e:
                    website = ''
                    pass
                
                

            except Exception as e:
                print (e)
                pass
                flag = False
            
            if flag is True:
                print ( 'No: {}, Saving data to database'.format(instance_index))
                issue = CrawelIssue.objects.create(
                    # user_id = request.user.id,
                    keyword = keyword, 
                    city_name = city_name, 
                    # crawel_number = crawel_number, 
                    instance_index = instance_index, 
                    title = title, 
                    rating = rating, 
                    votes = votes, 
                    contact = contact, 
                    address = address, 
                    website = website,
                    )

                instance_index += 1

    

    
    return ' scrabbing success!'