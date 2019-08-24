from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

score = {}

# an instance of Chrome
driver = webdriver.Chrome('E:/SOFTWARES/chromedriver')

#  login to HACKERRANK

driver.get('https://www.hackerrank.com/dashboard')

driver.maximize_window() #For maximizing window

login_btn =  driver.find_element_by_xpath('//button[normalize-space()="Log In"]')
login_btn.click()

username_input = driver.find_element_by_id('input-1')
password_input = driver.find_element_by_id('input-2')

username_input.send_keys('someone@something.com')
password_input.send_keys('*****')
password_input.send_keys(Keys.ENTER)

# get the contest leaderboard

def get_leaderboard(contestlink,leaderboard):
    try:
        error404 = driver.get_elements_by_class_name('e404-view')
        return "404"
    except AttributeError:
        driver.get('https://www.hackerrank.com/' + contestlink + leaderboard)
        driver.implicitly_wait(10) #gives an implicit wait for 10 seconds
        table_div = driver.find_element_by_id("leaders")
        divs = table_div.find_elements_by_class_name('leaderboard-list-view')
        for div in divs:
            parent_div      = div.find_elements_by_class_name('leaderboard-row')[0]
            divs_           = parent_div.find_elements_by_tag_name('div') #6 child divs in each row
            username_div    = divs_[1]
            p               = username_div.find_element_by_tag_name('p')
            a               = p.find_element_by_tag_name('a')
            hackerrank_id   = a.get_attribute('data-attr1')
            score_div       = divs_[3]
            p               = score_div.find_element_by_tag_name('p')
            score           = p.get_attribute('innerHTML').strip()           
            print(hackerrank_id,score)

#   CONTEST LINK
contestlink = "t13axxx"
for i in '12345678':
    get_leaderboard(contestlink,"/leaderboard/" + i)
