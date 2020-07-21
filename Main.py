from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

from contestInfo import ContestInfo
from writeScore import writeScore

class Main:
    def __init__(self):
    
        # an instance of Chrome
        self.driver = webdriver.Chrome('D:/SOFTWARES/chromedriver')
        self.login()
        self.begin()

    def login(self):
        '''
        This function is used to login to the Hackerrank platform. It declares an instance of Chrome, 
        which is shared by all functions till the end.
        '''
        self.driver.get('https://www.hackerrank.com/dashboard')
        self.driver.maximize_window() #For maximizing window
        time.sleep(5)
        login_btn =  self.driver.find_element_by_xpath('//button[normalize-space()="Log In"]')
        login_btn.click()

        time.sleep(5) #take a 5

        username_input = self.driver.find_element_by_id('input-1')
        password_input = self.driver.find_element_by_id('input-2')

        username_input.send_keys('gcfl@gla.ac.in')
        password_input.send_keys('gla@1234')
        password_input.send_keys(Keys.ENTER)

    def begin(self):
        '''
        This function is called after loggin in to the Hackerrank platform. It begins the 
        task of finding out information regarding the contest(s) & then writing the scores to 
        an excel file.
        '''

        contests = ['tp-olt-4','tp-olt-5','tp-olt-6']
        cnt = 4

        # get information about the contest using get_contest_info() function of ContestInfo class.
        infoObj = ContestInfo(self.driver,Keys)

        for contest in contests:
            infolist = infoObj.get_contest_info(contest)

            #get the leaderboard & write it to an excel file using write_scores() function of writeScore class.
            ws = writeScore(self.driver)
            ws.write_scores(cnt, *infolist)
            cnt += 1

        #close the last remaining Chrome tab.
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()

Main()

'''
NOTE: currently, begin() method of Main class, only writes the scores for a single contest, 
however, it can be modified to handle multiple no of contests, synchonously, using a simple loop.
'''
