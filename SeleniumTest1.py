"""
https://github.com/mozilla/geckodriver/releases

driver.find_element_by_xpath
driver.find_elements_by_xpath
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time
import re
from os.path import expanduser
import boulder_valley


driver = webdriver.Firefox()
"""
!!!   creds file needs to be configurable and needs to support windows paths  !!!!

"""


home_dir = expanduser("~")

user = ""
password = ""


def read_creds():
    global user
    global password
    with open(home_dir + "/.planetary_vegetation/creds.dat") as f1:
        data = f1.read()
        x = data.split("\n")
        user = x[0]
        password = x[1]

def login():
    driver.get("http://twitter.com/login")

    print( driver.title )
    time.sleep(5)
    #inputElement1 = driver.find_element_by_class_name("js-username-field")
    inputElement1 = driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/form/div/div[1]/label/div[2]/div/input")
    #inputElement2 = driver.find_element_by_class_name("js-password-field")
    inputElement2 = driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/form/div/div[2]/label/div[2]/div/input")
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
    """
        - search for tweets by keyword
        - follow users for top x tweets
        - follow x of that users followers

    """
    links = []

    # load Users from DB
    current_followers =
    current_following =
    # get most up to date followers and update db



    driver.get("https://twitter.com/search?q=" + search_term + "&src=typed_query")
    time.sleep(5)

    """
    x.send_keys(search_term)
    time.sleep(2)
    x.submit()
    """


    users_who_posted = []
    users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div[1]/div/article/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/a/div/div[2]/div/span").text)
    users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div[2]/div/article/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/a/div/div[2]/div/span").text)
    users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div[3]/div/article/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/a/div/div[2]/div/span").text)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div[4]/div/article/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/a/div/div[2]/div/span").text)
    users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div[5]/div/article/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/a/div/div[2]/div/span").text)

    print(users_who_posted)
    time.sleep(5)

    for u in users_who_posted:
        REMOVE THE @ sign from username
        driver.get("https://twitter.com/CatsGroupie" + u )
        time.sleep(5)
    https://twitter.com/CatsGroupie
    # load followers list
    # check if in followers list
    # follow
    follow_button = driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div[2]/div/div/div/span/span")
    follow_button.click()
    # add to DB of followed people
    check this users followers
    https: // twitter.com / CatsGroupie / followers
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[4]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[5]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
time.sleep(0.5)
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[4]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
    driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div[5]/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")

def follow(user_profile):
    ##
    ## gert user_profile page
    element = driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div[2]/div/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div[3]/div/div/div/span/span")
    element.click()
    time.sleep(10)
    ### limits on how many follows
    ### check if they follow people first ( they follow over 500 )


def get_user_followers(user_profile_link):
    """
        !!!!!!!!!!!! needs some debugging !!!!!!!!!!!11
    """
    links = []
    driver.get(user_profile_link + "/followers")
    time.sleep(5)
    user_list_xpath = "/html/body/div/div/div/div/main/div/div[2]/div/div[1]/div/div[2]/section/div/div/div"
    link_xpath = ".//div[1]/div/div/div/div[2]/div/div[1]/a"
    x = driver.find_elements_by_xpath(user_list_xpath)
    print(x)
    for y in x:
        try:
            z1 = y.findelement(link_xpath)
            print(z1.get_attribute('href'))
            links.append(z1.get_attribute('href'))
        except:
            print('ERROR - in get_user_followers()')
            pass
        finally:
            pass
    print("done getting user followers")
    return links


def add_user_to_db():
    pass

def is_user_following():
    pass

def am_i_following():
    pass

def is_user_blacklisted():   # <== when I unfollow
    pass

def black_list_user():       # <=== when I unfollow
    pass

def update_user_followed():
    pass

def update_i_followed():
    pass



read_creds()
login()
time.sleep(2)
stats()
time.sleep(2)
l1 = search("kittens")   # returns list of user profiles that posted a search
print(l1)
for i in l1:
    time.sleep(2)
    l2 = get_user_followers(i)   # returns list of user profiles that followed this one person

#total everything together from both previous functions and pass to follow()


time.sleep(1000)
driver.quit()

