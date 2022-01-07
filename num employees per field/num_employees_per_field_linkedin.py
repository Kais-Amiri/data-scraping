from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt



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


def how_many_employees(driver, search_key):
    url = "https://www.linkedin.com/company/amazon/people/?keywords="+search_key
    driver.get(url)
    time.sleep(3)
    number_of_employees = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[1]/div[1]/span').text.split(' ')[0].replace(' ','')
   
    return number_of_employees

if __name__ == '__main__':

    #path of chromdriver in your pc
    PATH = Service("C:\Program Files\chrome _driver\chromedriver.exe")


    #Creating a webdriver instance
    driver = webdriver.Chrome(service = PATH)

    #write your email
    email_linkedin = ""
    #write your password
    password_linkedin = ""

    save_path = "C:/Users/Desktop/save/linkedin"

    search_keywords = ["Software", "Hardware", "Data science"]
    num_employees=[]

    

    signin_linkedin(driver, email_linkedin, password_linkedin)

    for search_key in search_keywords:
        if ' ' in search_keywords:
            search_key= search_key.replace(' ', "%20")
        num = how_many_employees(driver, search_key).encode('ascii', 'ignore').decode("utf-8")
        num_employees.append(num)


    df = pd.DataFrame(list(zip(search_keywords, num_employees)),columns =['Fields', 'Number of employees'])
    df.to_csv('Employees_per_field.csv', index=True, encoding='utf-8')

    

    df["Number of employees"]  = pd.to_numeric(df["Number of employees"])

    sbn.barplot(x='Fields', y='Number of employees', data=df).set(title="Total number of employees per field : Software, Hardware and Data science")
    plt.show()