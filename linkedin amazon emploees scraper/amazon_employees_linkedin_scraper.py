from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os
import json
import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt
import numpy as np


def signin_linkedin(driver, linkedin_email, linkedin_password):

    driver.get("https://linkedin.com/uas/login")
    time.sleep(3)
    
    username = driver.find_element_by_id("username")

    username.send_keys(linkedin_email)

    password = driver.find_element_by_id("password")

    password.send_keys(linkedin_password)		

    driver.find_element_by_xpath("//button[@type='submit']").click()

    driver.maximize_window()

    time.sleep(3)

def scrape_employees_one_page(driver):

    all_employees_one_page = []
    def scrape_one_employee(employee):

        one_employee = {}

        try:
            one_employee["name"]= employee.find_element_by_css_selector("span[aria-hidden='true']").text
                
        except Exception:
            one_employee["name"]= ""

        try:
            one_employee["title"] = employee.find_element_by_class_name("entity-result__primary-subtitle").text
        except Exception:
            one_employee["title"] =""

        try:
            one_employee["location"] = employee.find_element_by_class_name("entity-result__secondary-subtitle").text
        except Exception:
            one_employee["location"] =""

        return one_employee
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
    
    employees = driver.find_elements_by_class_name("entity-result__item")
    
    for employee  in employees:
        employee_data = scrape_one_employee(employee)
        all_employees_one_page.append(employee_data)

    return all_employees_one_page


def number_of_pages(driver, url):
    try:
        driver.get(url)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        footer = driver.find_elements_by_class_name("artdeco-pagination__indicator")

        number_of_pages = footer[-1].find_element_by_tag_name("span").text
        
        return int(number_of_pages)

    except Exception:
        return 100



if __name__ == '__main__':

    #path of chromdriver in your pc
    PATH = Service("C:\Program Files\chrome _driver\chromedriver.exe")


    #Creating a webdriver instance
    driver = webdriver.Chrome(service = PATH)

    #write your email
    email_linkedin = ""
    #write your password
    password_linkedin = ""

    all_employees = []
    #folder path where you want to save the json file
    save_path = ""

    search_keywords = ["Chip"]

    

    signin_linkedin(driver, email_linkedin, password_linkedin)

    

    for search_keyword in search_keywords:
        if ' ' in search_keyword:
            search_keyword = search_keyword.replace(' ', "%20")
        url_amazon_employees = "https://www.linkedin.com/search/results/people/?currentCompany=%5B%221586%22%2C%2217411%22%2C%2212227%22%2C%2249318%22%2C%22167364%22%2C%2216551%22%2C%2214951%22%2C%222649984%22%2C%2246825%22%2C%222320329%22%2C%22208137%22%2C%2234924%22%2C%2261712%22%2C%22451028%22%2C%2247157%22%2C%22111446%22%2C%2221433%22%2C%222382910%22%2C%2271099%22%2C%22860467%22%5D&keywords=amazon%20"+search_keyword+"&origin=GLOBAL_SEARCH_HEADER&sid=aZU"
        
        for page in range(1, number_of_pages(driver, url_amazon_employees)+1):
            current_url ="https://www.linkedin.com/search/results/people/?currentCompany=%5B%221586%22%2C%2217411%22%2C%2212227%22%2C%2249318%22%2C%22167364%22%2C%2216551%22%2C%2214951%22%2C%222649984%22%2C%2246825%22%2C%222320329%22%2C%22208137%22%2C%2234924%22%2C%2261712%22%2C%22451028%22%2C%2247157%22%2C%22111446%22%2C%2221433%22%2C%222382910%22%2C%2271099%22%2C%22860467%22%5D&keywords=amazon%20"+ search_keyword +"&origin=GLOBAL_SEARCH_HEADER&page="+ str(page)+"&sid=jc*"
            driver.get(current_url)
            time.sleep(3)
            all_employees.extend(scrape_employees_one_page(driver))

        with open(os.path.join(save_path,'Amazon_'+search_keyword+ '_employees_linkedin'+'.json'), 'w') as outfile:
            json.dump(all_employees, outfile, indent=4)

        df = pd.DataFrame(all_employees, columns=['name', 'title', 'location'])
        df.to_csv('Amazon_'+ search_keyword+ '_employees_linkedin.csv', index=True, encoding='utf-8')
#filter chip employees 
    df["title"] = np.where(df["title"].str.find("Chip")>-1,"Amazon Chip Employee",df["title"][df.index])

    employees_types = ["Amazon Chip Employee"]
    subdf = df.loc[df['title'].isin(employees_types), :]
#plot there geographical distribution
    sbn.stripplot(x="title", y="location", data=subdf, hue="title").set(title="Geographical distribution of Chip designers")
    plt.show()