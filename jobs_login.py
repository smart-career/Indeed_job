import sys

from selenium import webdriver
import time
import json
import random

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://secure.indeed.com/account/login?")
driver.set_window_size(1024, 600)
driver.maximize_window()
time.sleep(2)
# LOGIN CODE
email = ""
password = ""
try:
    enter_email = driver.find_element_by_id("login-email-input")
    for character in email:
        enter_email.send_keys(character)
        time.sleep(random.random())
    time.sleep(random.random())
except:
    print("Something Went Wrong")
    sys.exit()
try:
    enter_password = driver.find_element_by_id("login-password-input")
    for character in password:
        enter_password.send_keys(character)
        time.sleep(random.random())
    time.sleep(random.random())
    enter_password.send_keys(Keys.ENTER)
except:
    print("Something Went Wrong")
    sys.exit()
try:
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.ID, "pageHeaderText")))
except TimeoutException as es:
    print("Unable to Login. Please try again")
    sys.exit(1)

driver.get("https://www.indeed.com")
try:
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.ID, "text-input-what")))
except TimeoutException as es:
    print("Invalid Indeed Page:")
    sys.exit(1)

# SEARCH JOB FOR A LOCATION

job_name = ""
location = ""

job_name = input("Please enter job to search:")
location = input("Enter location:")


try:
    enter_job = driver.find_element_by_id("text-input-what")
    enter_job.clear()
    enter_job.send_keys(Keys.CONTROL + "a")
    enter_job.send_keys(Keys.DELETE)
    for character in job_name:
        enter_job.send_keys(character)
        time.sleep(random.random())
    time.sleep(random.random())

except:
    print("Invalid Indeed Page:")
    sys.exit(1)
try:
    enter_location = driver.find_element_by_id("text-input-where")
    enter_location.clear()
    enter_location.send_keys(Keys.CONTROL + "a")
    enter_location.send_keys(Keys.DELETE)
    for character in location:
        enter_location.send_keys(character)
        time.sleep(random.random())
    time.sleep(random.random())
    enter_location.send_keys(Keys.ENTER)
except:
    print("Invalid Indeed Page:")
    sys.exit(1)

time.sleep(3)
data = {}
data['Jobs'] = []
loop = 1
count = 0
while loop != 2:
    try:
        main_class = driver.find_elements_by_xpath("//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard']")
    except Exception as es:
        print(es)
        print("No jobs Found")
        sys.exit(1)
    else:
        job_title = " "
        company = " "
        ratings = " "
        location = " "
        summary = " "
        pay = " "
        days = []

        try:
            day = driver.find_elements_by_xpath("//span[@class = 'date']")
        except:
            pass
        for i in range(0, len(main_class)):
            days.append(day[i].text)
        print(days)

        for i in range(0, len(main_class)-1):
            print(i)
            j = i+1
            job_title_xpath = "//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard'][" + str(j) + "]//div[@class = 'title']"
            try:
                job_title = driver.find_element_by_xpath(job_title_xpath)
                job_title = job_title.text
            except:
                job_title = " "
                pass

            company_xpath = "//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard'][" + str(j) + "]//span[@class = 'company']"
            try:
                company = driver.find_element_by_xpath(company_xpath).text
            except:
                company = " "
                pass

            ratings_xpath = "//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard'][" + str(j) + "]//span[@class = 'ratings']"
            try:
                ratings = driver.find_element_by_xpath(ratings_xpath).text
            except :
                ratings = "Not Provided"
                pass

            location_xpath = "//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard'][" + str(j) + "]//span[@class = 'location']"
            try:
                location = driver.find_element_by_xpath(location_xpath).text
            except:
                location = "No Provided"
                pass

            pay_xpath = "//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard'][" + str(j) + "]//span[@class = 'salary no-wrap']"
            try:
                pay = driver.find_element_by_xpath(pay_xpath).text
            except:
                pas = " "
                pass
            date_xpath = "//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard']["+ str(j)+ "]//span[@class = 'date']"
            try:
                date = driver.find_element_by_xpath(date_xpath).text
            except:
                date = " "
                pass

            get_summary_xpath = "//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard'][" + str(j) + "]"
            try:
                driver.find_element_by_xpath(get_summary_xpath).click()
                time.sleep(1)
                summary = driver.find_element_by_xpath("//div[@id = 'vjs-desc']").text
                summary = summary.translate({ord(i): None for i in '\n'})
            except:
                summary = " "
                pass

            print(job_title)
            print(company)
            print(ratings)
            print(location)
            print(pay)
            print(date)
            print(summary)

            print("--------------")
            time.sleep(1)

            data['Jobs'].append({
                'Job Title': job_title,
                'Company Name': company,
                'Rating': ratings,
                'Location': location,
                'Salary': pay,
                'Date': date,
                'Job Description': summary
            })
            with open('Output.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
    try:
        next = driver.find_elements_by_xpath("//span[@class='np']")
        if len(next) == 1:
            next[0].click()
        else:
            next[1].click()
        WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard']")))
        count = count +1
    except:
        loop = 2
        print(loop)
    # if count == 1:
    #     loop = 2

print('\nSTATUS: Scraping complete. Check "Output.json" for scraped data')
print('STATUS: Press any key to exit scraper')
exit = input('')
driver.quit()
