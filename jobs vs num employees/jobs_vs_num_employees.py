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


def how_many_employees_linkedin(driver, search_key):
    if ' ' in search_key:
        search_key= search_key.replace(' ', '%20')
    url = "https://www.linkedin.com/company/amazon/people/?keywords="+search_key
    driver.get(url)
    time.sleep(3)
    number_of_employees = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[1]/div[1]/span').text.split(' ')[0].replace(' ','')
    
    return number_of_employees

#signin glassdoor
def Signin_glassdoor(driver, email_glassdoor, password_glassdoor):
    url = 'https://www.glassdoor.com/profile/login_input.htm'
    driver.get(url)

    email_field = driver.find_element_by_name('username')
    password_field = driver.find_element_by_name('password')

    submit_btn = driver.find_element_by_xpath('//button[@type="submit"]')

    email_field.send_keys(email_glassdoor)
    password_field.send_keys(password_glassdoor)

    submit_btn.click()

    time.sleep(10)

#--------------- end signin glassdoor--------------------



def how_many_jobs_glassdoor(driver, search_jobs):
    if ' ' in search_jobs:
        search_jobs= search_jobs.replace(' ', '%20')
    url= "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=amazon%20"+search_jobs+"&locT=&locId=0&locKeyword=&srs=RECENT_SEARCHES"
    driver.get(url)
    num_jobs = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/div[1]/div/div/h1').text.split(' ')[0]

    return num_jobs


if __name__ == '__main__':

    #path of chromdriver in your pc
    PATH = Service("C:\Program Files\chrome _driver\chromedriver.exe")


    #Creating a webdriver instance
    driver = webdriver.Chrome(service = PATH)

    #write your email
    email_linkedin = ""
    #write your password
    password_linkedin = ""

    #write your email
    email_glassdoor = ""
    #write your password
    password_glassdoor = ""

    search_key= ["Chip design"]

    num_emp=[]
    num_jobs=[]


    signin_linkedin(driver, email_linkedin, password_linkedin)
    num1 = how_many_employees_linkedin(driver, search_key[0])
    num_emp.append(int(num1))
    Signin_glassdoor(driver, email_glassdoor, password_glassdoor)
    num2 = how_many_jobs_glassdoor(driver, search_key[0])
    num_jobs.append(int(num2))


    df = pd.DataFrame(list(zip(search_key, num_jobs ,num_emp)), columns=["Field", "jobs", "number of employees"])
    df.to_csv('num_employees_and_jobs.csv', index=False, encoding='utf-8')

    sbn.set(style='white')

    #create stacked bar chart
    df.set_index('Field').plot(kind='bar', stacked=True, color=['steelblue', 'red'])

    plt.show()