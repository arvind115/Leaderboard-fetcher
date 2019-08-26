from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pandas as pd

scores = {}

# an instance of Chrome
driver = webdriver.Chrome('E:/SOFTWARES/chromedriver')

#  login to HACKERRANK

driver.get('https://www.hackerrank.com/dashboard')
driver.maximize_window() #For maximizing window
driver.implicitly_wait(5) #take a 5
login_btn =  driver.find_element_by_xpath('//button[normalize-space()="Log In"]')
login_btn.click()

driver.implicitly_wait(5) #take a 5

username_input = driver.find_element_by_id('input-1')
password_input = driver.find_element_by_id('input-2')

username_input.send_keys('########')
password_input.send_keys('#####')
password_input.send_keys(Keys.ENTER)

# get the contest leaderboard

def get_leaderboard(contestlink,leaderboard):
    url = 'https://www.hackerrank.com/' + contestlink + leaderboard
    driver.get(url)
    driver.implicitly_wait(7) #wait for 7
    try:
        table_div = driver.find_element_by_id("leaders")
    except:
        try:
            table_div = driver.find_element_by_id("leaders")
        except:
            pass
        print("some error occured. Retrying")
        #get_leaderboard(contestlink,leaderboard)
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
            scores[hackerrank_id] = int(score[:score.index('.')])

#   CONTEST DETAILS
# 1.  contest name
# 2.  contest date
# 3.  contest total score
# 4.  leaderboard tiles at bottom 
contestlink = "t23fcxx"
date = '14-Aug-19'
total = 80
pagetiles = 7
test = 'Test2'

for i in range(1,pagetiles+1):
    res = get_leaderboard(contestlink,"/leaderboard/" + str(i))

f = pd.read_excel(r'C:\Users\Arvind\Desktop\gcfl.xlsx')

for col in f.columns:
    if 'Unnamed' in col:
        f.drop([col], axis=1, inplace=True)

f['Total '] = total

for key in scores.keys():
    #row = f.loc[f['HackerRank Id'] == key].index
    f.loc[f.loc[f['HackerRank Id'] == key].index,test] = date
    f.loc[f.loc[f['HackerRank Id'] == key].index,'Score'] = scores[key]

f.to_excel(r'C:\Users\Arvind\Desktop\gcfl.xlsx')
print("done")
