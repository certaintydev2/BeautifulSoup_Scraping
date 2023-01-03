# Import required libraries 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time


# add user agent
headers = ({"User-Agent":"XXXXX"}) 

# define chromedriver path
chromeDriver = "XXX\\chromedriver.exe"

# create browser using chromeDriver
browser = webdriver.Chrome(executable_path=chromeDriver)

link_list,web = [], []
  
# create data frame for storing extracted data     
df = pd.DataFrame(columns=['Name', 'Logo', 'Address', 'Phone Number','Contact', 'Fax', 'Website', 'Email', 'VAT number'])

def data_details(url_link):
    if url_link.startswith("https"):
        if url_link not in link_list:
            link_list.append(url_link)
            get_url = requests.get(url_link, headers=headers, timeout=20)
            
            # create soup of url
            soup = BeautifulSoup(get_url.text, "html.parser")
            
            # access elements based on class, id and tag-name
            itemscope_data = soup.find("div", {"class": "XXXXXX"})

            if itemscope_data.find("img", {"id": "XXXXXX"}) != None:
                logo = "https://XXXXXX"+itemscope_data.find("img", {"id": "XXXXXX"})["src"]
            else:
                logo = "None"

            if itemscope_data.find("h1") != None:
                name = itemscope_data.find("h1").text.strip()
            else:
                name = "None"

            innerContainer = soup.find("div", {"class": "XXXXXX"})

            titles = innerContainer.find_all("div", {"class":"XXXXXX"})
            
            number, fax, website, VATnumber, contact, email = "None", "None", "None", "None", "None", "None"
            for data in titles:
                if data.text.strip() == 'Telephone':
                    if data.find_next("div", {"id": "XXXXXX"}) != None:
                        number = data.find_next("div", {"id": "XXXXXX"})["onclick"].split(",")[1]

                elif data.text.strip() == 'Fax':
                    if data.find_next("div", {"class":"XXXXXX"}) != None: 
                        fax = data.find_next("div", {"class":"XXXXXX"}).text.strip()

                elif data.text.strip() == 'Website':
                    if data.find_next("div", {"class":"XXXXXX"}) != None:
                        website = data.find_next("div", {"class":"XXXXXX"}).text.strip()
                        try:
                            browser.get("https://"+website) 
                            browser.set_page_load_timeout(20) 
                        except: continue

                        word_list = ['Registered', 'registration', 'VAT']
                        text_data_website = browser.find_element(By.XPATH, "XXXXXX").text.splitlines()
                        for line in text_data_website:
                            for word in word_list:
                                if word in line:
                                    VATnumber = line
                                    break

                elif data.text.strip() == 'Contact':
                    if data.find_next("div", {"class":"XXXXXX"}) != None:
                        contact = data.find_next("div", {"class":"XXXXXX"}).text.strip()

                elif data.text.strip() == 'Email':
                    if data.find_next("div", {"class":"XXXXXX"}) != None:
                        div_data = data.find_next("div", {"class":"XXXXXX"})
                        email_link = str(div_data.find("script").text.strip().split("(")[2]).split(",")[0]
                        email = ""
                        for i in range(1,len(email_link)-1):
                            li = ord(email_link[i])
                            email += chr(li - 1)

            addr = innerContainer.find("div", {"class" : "XXXXXX"})
            if addr != None:
                if addr.text.strip() == 'Address':
                    address = addr.find_next("div", {"itemprop":"XXXXXX"}).text.strip()
            else:
                address = "None"
            
            soup_href_list = [a.find("a")['href'] for a in soup.find_all("div", {"class": "XXXXXX XXXXXX XXXXXX"})]
            
            # returning the data
            return [name, logo, address, number, contact, fax, website, email, VATnumber], soup_href_list


# looping for pagination
for i in range(1, 10):        
    get_urls = requests.get("https://XXXXXX"+str(i)+"/XXXXXX", headers=headers, timeout=20)
    
    # create soup of url
    bs = BeautifulSoup(get_urls.text, "html.parser")

    # access elements using id, class and tag-name
    section_data = bs.find("div", {"id": "XXXXXX"})
    ancher_tags = section_data.find_all("a")

    soup_href_list = []
    
    # used list comprehension for storing data od archer_tags
    href_list = [a['href'] for a in ancher_tags]
    
    result = map(data_details, href_list)
    for lst in result:
        if lst != None:
            df.loc[len(df)] = lst[0]
            soup_href_list.extend(lst[1])

    if soup_href_list:
        # used map function for speed up the process
        result2 = map(data_details, list(set(soup_href_list)))
        
        for lst in result2:
            if lst != None:
                df.loc[len(df)] = lst[0]

browser.close()

# create csv file using dataframe
df.to_csv('XXXXXX.csv')