from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
import json
import random




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

#------------------ glassdoor scraper function -----------
def scrape_review(reviewsUrl,driver,save_path):
   
   #test the last page of reviews
    def last_page():
        try:
            footer = driver.find_element_by_class_name('paginationFooter').text
            a = footer.split(' ')
            if (int(a[3]) >= int(a[5].replace(",", "").split('.00')[0])):
                return True
            else:
                return False
        except Exception:
            return True

    #srape rating
    def scrape_rating(review):
        try:
            Rating = review.find_element_by_class_name('ratingNumber').text
        except Exception:
            pass
        return Rating

    # scrape employee status
    def scrape_employee_status_experience(review):
        try:
            se = review.find_element_by_xpath("div/div/div/div/span").text.split(',')
            status = se[0].strip()
            experience = se[1].strip()
        except Exception:
            status = ""
            experience = ""
        return status,experience

    # scrape review title
    def scrape_review_title(review):
        try:
            title = review.find_element_by_xpath(".//a[@class='reviewLink']").text
        except Exception:
            title = ""
        return title

    # scrape date and employee title
    def scrape_date_employee_title(review):
        try:
            date_title = review.find_element_by_class_name('authorInfo').text.split('-')
            date = date_title[0].strip()
            title = date_title[1].strip()
        except Exception:
            date = ""
            title = ""
        return date,title
    
    # scrape employee location
    def scrape_location(review):
        try:
            location = review.find_element_by_class_name('authorLocation').text
        except Exception:
            location = ""
        return location

    # scrape recommendation 

    def scrape_recommendation(review):
        recommendation = {}
        try:
            recommendation_list = review.find_element_by_class_name('recommends').find_elements_by_xpath("div")
            for r in recommendation_list:
                score = recommendationList[r.find_element_by_xpath('span').get_attribute('class')]
                name = r.find_element_by_xpath('span/following-sibling::span').text.strip()
                recommendation[name] = score
        except Exception:
            pass
        return recommendation

    # scrape pros cons advise from review
    def scrape_pros_cons_advice(review):
        try:
            expand = review.find_element_by_xpath(".//div[contains(text(),'Continue reading')]").click()
        except Exception:
            pass
        try:
            pros = review.find_element_by_xpath(".//span[@data-test='pros']").text
        except Exception:
            pros = ""
        try:
            cons = review.find_element_by_xpath(".//span[@data-test='cons']").text
        except Exception:
            cons = ""
        try:
            advice = review.find_element_by_xpath(".//span[@data-test='advice-management']").text
        except Exception:
            advice = ""
        return pros,cons,advice


    # scrape helpful
    def scrape_helpful(review):
        num_help = 0
        try:
            helpful = review.find_element_by_class_name('common__EiReviewDetailsStyle__socialHelpfulcontainer').text
            if 'person' in helpful:
                n = int(helpful.split(' ')[0])
        except Exception:
            pass
        return num_help

    # scrape review one page
    def scrape_review_one_page(reviews,reviewsAll):
        for i in range(len(reviews)):
            r = reviews[i]
            review = {}    
            review['rating'] = scrape_rating(r)
            review['status'],review['experience'] = scrape_employee_status_experience(r)
            review['review_title'] = scrape_review_title(r)
            review['date'],review['employee_title'] = scrape_date_employee_title(r)
            review['location'] = scrape_location(r)
            review['recommendation'] = scrape_recommendation(r)
            review['pro'],review['con'],review['advice'] = scrape_pros_cons_advice(r)
            review['helpful'] = scrape_helpful(r)
            
            reviewsAll.append(review)
    
        return reviewsAll

    reviewsAll = []
    noFinished = True
    j=1

    driver.get(reviewsUrl)

    while noFinished:
        reviews = driver.find_elements_by_class_name('empReview')
        reviewsAll = scrape_review_one_page(reviews,reviewsAll)
        
        j +=1
        
        nextPage = reviewsUrl.split('.htm')[0]+ '_P'+str(j)+'.htm?filter.iso3Language=eng'
        driver.get(nextPage)
        
        time.sleep(random.uniform(2,3))
        #if you want to scrape all pages
        #if last_page():
        #if you want to scrape 50 pages , j==50
        if j==50:
            noFinished = False
            reviews = driver.find_elements_by_class_name('empReview')
            reviewsAll = scrape_review_one_page(reviews,reviewsAll)
            with open(os.path.join(save_path,'glassdoor_reviews_'+'.json'), 'w') as outfile:
                json.dump(reviewsAll, outfile, indent=4)
            df = pd.DataFrame(reviewsAll, columns=['rating', 'status', 'experience', 'review_title', "date", "employee_title", "location", "pro", "con", "advice"])
            df.to_csv('glassdoor_reviews.csv', index=True, encoding='utf-8')
            break



if __name__ == '__main__':

    #path of chromdriver in your pc
    PATH = Service("C:\Program Files\chrome _driver\chromedriver.exe")


    #Creating a webdriver instance
    driver = webdriver.Chrome(service = PATH)


    #maximize the browser window 
    driver.maximize_window()

    #write your email
    email_glassdoor = ""
    #write your password
    password_glassdoor = ""


    recommendationList = {}
    recommendationList['SVGInline css-10xv9lv d-flex'] = ""
    recommendationList['SVGInline css-hcqxoa d-flex'] = 1
    recommendationList['SVGInline css-1kiw93k d-flex'] = -1
    recommendationList['SVGInline css-1h93d4v d-flex'] = 0

    #path where saving json file
    save_path = "C:/Users/Desktop/test_data_scraping"

    reviewsUrl="https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm"
    
    Signin_glassdoor(driver, email_glassdoor, password_glassdoor)
    scrape_review(reviewsUrl,driver,save_path)