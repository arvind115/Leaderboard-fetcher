from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import pandas as pd
import time

class writeScore:
    def __init__(self,driver):
            self.driver = driver
            self.scores = {}

    def readLeaderboard(self):
        '''
        This functions reads the currently open tab of the leaderboard & records it in scores{} dict.
        '''
        driver = self.driver
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        table_div = WebDriverWait(driver, 8,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, 'leaders')))
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
                self.scores[hackerrank_id] = int(score[:score.index('.')])
        driver.implicitly_wait(3)

    def write_scores(self,testno,contestlink,date,total,pagetiles,first = True):
        '''
        Work of this funcion is done in two loops. First loop runs over no of pagetiles i.e. the total no of 
        leaderboard pages there are, all are opened in a go one after another in a new tab. Its important to 
        use new tabs to avoid errors due to delay in DOM loading.
        '''
        driver = self.driver
        for i in range(1,pagetiles+1):
            driver.implicitly_wait(2)
            # open a new tab
            driver.execute_script("window.open('');")
            time.sleep(2)
            #focus on the last tab...
            driver.switch_to.window(driver.window_handles[-1])
            url = 'https://www.hackerrank.com/' + contestlink + '/leaderboard/' + str(i)
            driver.get(url)
            time.sleep(2)
            driver.implicitly_wait(2) #wait for 2
    

        for i in range(pagetiles):
            driver.implicitly_wait(5)
            #focus on the last tab...
            driver.switch_to.window(driver.window_handles[-1])
            #read that tab's leaderboard
            self.readLeaderboard()
            #close it
            driver.close()
        
        self.writeToExcel(first,testno,contestlink,date,total)


    def writeToExcel(self,first,testno,contestlink,date,total):
        '''
        This function takes info of a contest & makes use of it while writing scores{} to an excel file.
        '''

        f = pd.read_excel(r'C:\Users\Arvind\Desktop\OLT_scores.xlsx')

        for col in f.columns:
            if 'Unnamed' in col:
                f.drop([col], axis=1, inplace=True)
        if first:
            f['Total'+str(testno)] = total  #do this only for the first contest for a particular TEST
            f['Score'+str(testno)] = 0      #do this only for the first contest for a particular TEST

        for key in self.scores.keys():
            f.loc[f.loc[f['HackerRank Id'] == key].index,'Test'+str(testno)] = date               #fill the date 
            f.loc[f.loc[f['HackerRank Id'] == key].index,'Score'+str(testno)] = self.scores[key]       #fills the score

        f.to_excel(r'C:\Users\Arvind\Desktop\OLT_scores.xlsx')

        print(contestlink,'done')
