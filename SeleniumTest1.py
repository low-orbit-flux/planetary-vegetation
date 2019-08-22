from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time


driver = webdriver.Firefox()
"""
!!!   creds file needs to be configurable and needs to support windows paths  !!!!

"""


user = ""
password = ""


def read_creds():
    global user
    global password
    with open("/home/user1/.planetary_vegetation/creds.dat") as f1:
        data = f1.read()
        x = data.split("\n")
        user = x[0]
        password = x[1]

def login():
    driver.get("http://twitter.com/login")

    print( driver.title )
    inputElement1 = driver.find_element_by_class_name("js-username-field")
    inputElement2 = driver.find_element_by_class_name("js-password-field")
    time.sleep(2)
    inputElement1.send_keys(user)
    time.sleep(2)
    inputElement2.send_keys(password)
    time.sleep(2)
    inputElement1.submit()

    try:
        WebDriverWait(driver, 10).until(EC.title_contains("Home"))
        print( driver.title )
    finally:
        pass

def stats():
    driver.get("https://twitter.com/Stegosa99042135")
    time.sleep(5)
    #followers = driver.find_element_by_link_text("Followers")
    followers = driver.find_element_by_xpath("/html/body/div")
    print(followers)

read_creds()
login()
time.sleep(2)
stats()
time.sleep(2)



time.sleep(1000)
driver.quit()

