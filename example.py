import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('/media/jhon/ccdab2e9-3b2f-4917-a374-6c99033c196c/home/jhon/Documentos/projects/justdial_data_extractor/.env/selenium/chromedriver')
driver2 = webdriver.Chrome('/media/jhon/ccdab2e9-3b2f-4917-a374-6c99033c196c/home/jhon/Documentos/projects/justdial_data_extractor/.env/selenium/chromedriver')

city = 'Ahmedabad'
category = 'Gym'
number_page = 2
instance_index = 0
for page in range(number_page):
    page = 'https://www.justdial.com/' + city + '/' + category + '/page-'+ str(page + 1)
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

            contacts = contacts +" " +  contact.find_element_by_class_name("tel").get_attribute("innerHTML")
            contacts = contacts.replace("<b>","")
            contacts = contacts.replace("</b>","")
            print(contacts)
            address = contact.find_element_by_class_name("lng_add").get_attribute("innerHTML")
            websites = contact.find_elements_by_css_selector(".mreinfp.comp-text")
            website = ""
            for ix,get_website  in enumerate(websites):
                if ix == 1:
                
                    website = get_website.find_element_by_tag_name("a").get_attribute("href")

        print ( 'No: {}, Saving data to database.'.format(instance_index))
        instance_index += 1

