from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time
import re


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
    following = "0"
    followers = "0"
    driver.get("https://twitter.com/Stegosa99042135")
    time.sleep(5)
    #followers = driver.find_element_by_link_text("Followers")
    data1 = driver.find_element_by_xpath("/html/body/div")
    m1 = re.search(data1.text, "\n(\d+) Following\n(\d)+Followers\n")
    if m1:
        following = m1.group(1)
        followers = m1.group(2)
    print("Following: " + following)
    print("Followers: " + followers)


def search(search_term):
    x = driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input")
    x.send_keys(search_term)
    time.sleep(2)
    x.submit()

read_creds()
login()
time.sleep(2)
stats()
time.sleep(2)
search("kittens")



time.sleep(1000)
driver.quit()

