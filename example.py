import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('/home/desarrollador/Documentos/.projects/justdial_data_extractor/.env/selenium/webdriver/chromedriver')
driver2 = webdriver.Chrome('/home/desarrollador/Documentos/.projects/justdial_data_extractor/.env/selenium/webdriver/chromedriver')

driver.get('https://www.justdial.com/Ahmedabad/Gyms/page-1');
elem = driver.find_element_by_tag_name("body")

no_of_pagedowns = 100

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1


post_elems = driver.find_element_by_id("srchpagination")
print(str(post_elems))
index = 1
isContact = False
for i in driver.find_elements_by_class_name("cntanr"):

    title = i.find_element_by_class_name("srtbyPic").get_attribute("title")
    rating = i.find_element_by_class_name("exrt_count").get_attribute("innerHTML")
    votes = i.find_element_by_class_name("lng_vote").get_attribute("innerHTML").strip(' \t\n\r')[0:5:1].strip()
    single_url = i.find_element_by_class_name("srtbyPic").get_attribute("href")
    contacts = ""
    driver2.get(single_url)
    elem2 = driver2.find_element_by_tag_name("body")
    elem2.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    for contact in elem2.find_elements_by_class_name("cmawht"):

        contacts = contacts + contact.find_element_by_class_name("tel").get_attribute("innerHTML")
        isContact = True
    print (str(index) + " -"+  contacts)
    #i.find_element_by_xpath('.//span[@class="exrt_count"]').text)
    index+=1
