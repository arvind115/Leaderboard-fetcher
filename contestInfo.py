import time
class ContestInfo:
    
    def __init__(self,driver,Keys):
        self.driver = driver
        self.Keys = Keys

    def get_contest_info(self,contest):
        ''' this function is used to get the information
            about a contest based on its name.
            It returns a list containing following items:
            contest     - the name of the contest itself, as passed
            date        - the date on which contest was held on Hackerrank.com
            max_score   - total score of all the problems included in the contest
            tiles       - no of leaderboard pages. One leaderboard page contains details of 10 participants. 
        '''
        driver = self.driver
        Keys = self.Keys
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        driver.get('https://www.hackerrank.com/administration/contests')
        time.sleep(5)
        searchbox = driver.find_element_by_class_name('search-query')
        searchbox.send_keys(contest)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(3)
        date = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/section/div[2]/div/a/div/div[4]/p').text
        tiles = int(driver.find_element_by_xpath('//*[@id="content"]/div/div/div/section/div[2]/div/a/div/div[6]/p').text)//10
        driver.get('https://www.hackerrank.com/contests/{0}/challenges'.format(contest))
        time.sleep(4)
        challenges = len(driver.find_elements_by_class_name('challenges-list-view'))
        max_score = challenges * 20
        return [contest,date,max_score,tiles]
