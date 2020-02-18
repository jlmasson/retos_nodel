import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import sys

if len(sys.argv) != 4:
    print("python main.py <user> <pass> <link>")
else:
    # get login credentials
    email = sys.argv[1]
    password = sys.argv[2]
    # email = input('Enter email: ')
    # password = input('Enter password: ')

    # get post url
    post_url = sys.argv[3]
    print(post_url)
    # post_url = input('Enter post url: ')

    # create a new Chrome session
    chromedriver_location = "../bin/chromedriver"
    driver = webdriver.Chrome(chromedriver_location)
    driver.maximize_window()

    # log in
    driver.get("https://www.facebook.com")
    search_field = driver.find_element_by_id("email")
    search_field.send_keys(email)
    search_field = driver.find_element_by_id("pass")
    search_field.send_keys(password)
    search_field.submit()

    print("Logged in as " + email)

    # navigate to the post url
    driver.get(post_url)

    existenReacciones = False

    while True:
        try:
            engagement_div = driver.find_element_by_css_selector("a[href*='/ufi/reaction']")
            driver.execute_script("arguments[0].click();", engagement_div)
            sleep(2)
            existenReacciones = True
            break
        except NoSuchElementException:
            existenReacciones = False
            break

    sleep(2)


    # switch to all engagement - not working
    # engagement_all = driver.find_element_by_css_selector("a[tabindex*='-1']")

    # print(engagement_all)

    if (existenReacciones):
        driver.execute_script("arguments[0].click();", engagement_div)

        # click see more until there no such option
        print("Loading all the users.")

        while True:
            print("Entré a buscar likes")
            try:
                viewMoreButton = driver.find_element_by_css_selector("a[href*='/ufi/reaction/profile/browser/fetch']")
                driver.execute_script("arguments[0].click();", viewMoreButton)
                sleep(2)
            except NoSuchElementException:
                break

        # invite users
        print("Inviting the users.")
        users = driver.find_elements_by_css_selector("a[ajaxify*='/pages/post_like_invite/send/']")
        sleep(1)
        invitedUsers = 0

        for i in users:
            user = driver.find_element_by_css_selector("a[ajaxify*='/pages/post_like_invite/send/']")
            driver.execute_script("arguments[0].click();", user)
            invitedUsers = invitedUsers + 1
            sleep(1)

        print('My job is done here. I have invited: ' + str(invitedUsers))
    else:
        print("No reactions found")
    # close the browser window
    driver.quit()