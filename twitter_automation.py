
import sys
import os
import subprocess
from twitter import *
import time
import datetime
import json
import sys
import os
#import FeedSource
sys.path.append(os.path.abspath("/home/user1/Desktop"))
#import boulder_valley
from pymongo import MongoClient
from bson.objectid import ObjectId


config = {}                 # global configs read from config file


def load_configs():
    if os.path.exists("main.config"):
        f = open("main.config", "r")
        config_data = f.read()
        f.close()
        config.update(json.loads(config_data))


def auth(user_info):
    #if not os.path.exists(MY_TWITTER_CREDS):
    #    oauth_dance("My App Namexxx", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

    twitter = Twitter(auth=OAuth(user_info["creds"]["accessToken"], user_info["creds"]["accessTokenSecret"],
                                 user_info["creds"]["consumerKey"], user_info["creds"]["consumerSecret"]))
    return twitter


def get_stats(twitterObj, user_info):
    followers = get_followers(user=user_info["username"], twitterObj=twitterObj)
    friends = get_friends(user=user_info["username"], twitterObj=twitterObj)
    return len(followers), len(friends)


def get_stats_db(user_info):
    client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
    db = client.planetaryVegetation
    friends = db.twitterUsers.find({"accountID": user_info["_id"], "friend.status": "started"})
    followers = db.twitterUsers.find({"accountID": user_info["_id"], "follow.status": "started"})
    follow_backs = db.twitterUsers.find({"accountID": user_info["_id"], "friend.status": "started", "follow.status": "started"})
    friends_not_following = db.twitterUsers.find(
        {"accountID": user_info["_id"], "friend.status": "started", "follow.status": {"$ne": "started"}})

    return friends.count(), followers.count(), follow_backs.count(), friends_not_following.count()


def log_stats_to_db(user_info):
    data = get_stats_db(user_info)

    client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
    db = client.planetaryVegetation
    ts = db.twitterStats

    log_this = {"accountID": user_info["_id"],
                "friends": data[0], "followers": data[1],
                "follow_backs": data[2], "friendsNotFollowing": data[3],
                "timestamp": datetime.datetime.utcnow()}
    ts.insert_one(log_this)
    print("adding stats")


def show_logged_stats(user_info):
    client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
    db = client.planetaryVegetation
    data = db.twitterStats.find({"accountID": user_info["_id"]})
    return data


def unfollow(user_info, twitterObj):
    client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
    db = client.planetaryVegetation
    friends_not_following = db.twitterUsers.find(
        {"accountID": user_info["_id"], "friend.status": "started", "follow.status": {"$ne": "started"}})

    HARDCODED_UNFOLLOW_LIMIT = 75
    c = 0
    for i in friends_not_following:
        print(i["twitterID"])
        twitterObj.friendships.destroy(user_id=i["twitterID"])
        time.sleep(1200)       # 1200 is every 20 minutes
        c += 1
        if c == HARDCODED_UNFOLLOW_LIMIT:
            break


def find_friends(user_info, twitterObj, topic):
    good_to_follow = []
    try:
        client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
        db = client.planetaryVegetation

        results = twitterObj.search.tweets(q=topic, count=100)
        print("[ID] [name] [screen_name] [protected] [followers] [friends]")
        print(40 * "=")
        for i in results["statuses"]:
            if not i["user"]["protected"]:
                # need to have at least 500 friends ( they follow people )
                # need to have at least 50 followers ( at lest some people follow them )
                if i["user"]["followers_count"] >= 50 and i["user"]["friends_count"] >= 500:
                    # DB Check - if already following, unfollowed, or following me
                    from_db = db.twitterUsers.find_one({"accountID": user_info["_id"], "twitterID": i["user"]["id"]})
                    if not from_db:
                        if i["user"]["id"] not in good_to_follow:   # don't log duplicates
                            print(str(i["user"]["id"]) + " [" + i["user"]["name"] + "] [" + i["user"][
                                "screen_name"] + "] "
                                  + str(i["user"]["protected"]) + " " + str(i["user"]["followers_count"]) + " "
                                  + str(i["user"]["friends_count"]))
                            good_to_follow.append(i["user"]["id"])
    except:
        pass
    return good_to_follow


def auto_follow(user_info, twitterObj, topic):
    friends_to_add = find_friends(user_info, twitterObj, topic)
    for i in friends_to_add:
        print("Adding: " + str(i))
        #twitterObj.friendships.create(user_id=i, follow="true")
        time.sleep(900)


def get_followers(twitterObj, user="" ):
    followers = twitterObj.followers.ids(screen_name=user)      #GET followers/ids     # get followers
    if followers["next_cursor"] != 0:
        print "\n\n\n\nWARNING - more followers exist, update code to handle these\n\n\n\n"
    return followers["ids"]


def get_friends(twitterObj, user=""):
    friends = twitterObj.friends.ids(screen_name=user)      #GET friends/ids     # get friends
    if friends["next_cursor"] != 0:
        print "\n\n\n\nWARNING - more friends exist, update code to handle these\n\n\n\n"
    return friends["ids"]


def load_db(twitter_user, twitter_id):
    auth_object1 = auth(user=twitter_user)             # get auth object for this user
    followers, friends = getStats(auth_object1, twitter_user)
    # print twitter_user + "    Followers: " + str(len(followers)) + "       Friends: " + str(len(friends))
    time1 = time.strftime("%Y-%m-%d %H:%M:%S")
    params = [('varchar', str(len(friends))), ('varchar', str(len(followers))), ('varchar', '0'), ('int', twitter_id), ('varchar', time1)]
    db_insert_status = boulder_valley.my_crud.insert_data("127.0.0.1", "root", "xxxxxxxxx", "campaigns", 'twitter_metrics', params)
    return str(len(followers)), str(len(friends)), db_insert_status


def load_db_all():
    results = ""
    output = boulder_valley.my_crud.print_all("127.0.0.1", "root", "xxxxxxxxxxx", "campaigns", 'twitter_accounts')
    for i in output:
        status = load_db(i[2], str(i[0]))

        results = results + str(i[0]) + " " + i[1] + " followers: " + status[0] + "following: " + status[1] + "\n"
    return results


def store_existing_users(twitterObj, user_info):
    """
    store existing friends and followers in the database
    """

    followers = get_followers(user=user_info["username"], twitterObj=twitterObj)
    friends = get_friends(user=user_info["username"], twitterObj=twitterObj)

    client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
    db = client.planetaryVegetation
    tu = db.twitterUsers

    for i in followers:
        from_db = db.twitterUsers.find_one({"accountID": user_info["_id"], "twitterID": i})
        if not from_db:        # user not stored yet
            user = {"accountID": user_info["_id"], "twitterID": i, "follow": {"status": "started", "startDate": datetime.datetime.utcnow()}}
            tu.insert_one(user)
            print("adding follower")
        else:                           # user already stored
            if "follow" in from_db:
                if "status" in from_db["follow"]:
                    if from_db["follow"]["status"] != "started":
                        tu.update({"_id": from_db["_id"]}, {"$set": {"follow.status": "started",
                                                                     "follow.startDate": datetime.datetime.utcnow()}},
                                  upsert=False)
                        print("updating follower")
                    else:
                        pass    # don't need to do anything, already set
                else:
                    tu.update({"_id": from_db["_id"]}, {"$set": {"follow.status": "started",
                                                                 "follow.startDate": datetime.datetime.utcnow()}},
                              upsert=False)
                    print("updating follower")
            else:
                tu.update({"_id": from_db["_id"]}, {"$set": {"follow.status": "started",
                                                             "follow.startDate": datetime.datetime.utcnow()}},
                          upsert=False)
                print("updating follower")

    for i in friends:
        from_db = db.twitterUsers.find_one({"accountID": user_info["_id"], "twitterID": i})
        if not from_db:
            user = {"accountID": user_info["_id"], "twitterID": i, "friend": {"status": "started", "startDate": datetime.datetime.utcnow()}}
            tu.insert_one(user)
            print("adding friend")
        else:
            """
                - make sure the fields exist, if not, add them and set to 'friend'
                  ( they might not exist, could just be a follower )
                - make sure the field is set to friend, if not, set it
            """
            if "friend" in from_db:
                if "status" in from_db["friend"]:
                    if from_db["friend"]["status"] != "started":
                        tu.update({"_id": from_db["_id"]},
                                  {"$set": {"friend.status": "started",
                                            "friend.startDate": datetime.datetime.utcnow()}}, upsert=False)
                        print("updating friend")
                    else:
                        pass  # don't need to do anything, already set
                else:
                    tu.update({"_id": from_db["_id"]},
                              {"$set": {"friend.status": "started", "friend.startDate": datetime.datetime.utcnow()}},
                              upsert=False)
                    print("updating friend")
            else:
                tu.update({"_id": from_db["_id"]},
                          {"$set": {"friend.status": "started", "friend.startDate": datetime.datetime.utcnow()}},
                          upsert=False)
                print("updating friend")

    return 0


def add_account(a):

    print a
    """
    just pass all of these things in order:

    username
    password
    email
    fname
    lname
    vertical
    notes
    consumerKey
    consumerSecret
    accessToken
    accessTokenSecret
    """


    account = {
        "username": a[0],
        "password": a[1],
        "email": a[2],
        "fname": a[3],
        "lname": a[4],
        "vertical": a[5],
        "notes": a[6],
        "creds": {
            "consumerKey": a[7],
            "consumerSecret": a[8],
            "accessToken": a[9],
            "accessTokenSecret": a[10]}}

    client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
    db = client.planetaryVegetation
    accounts = db.accounts
    accounts.insert_one(account)


def list_accounts():
    client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
    db = client.planetaryVegetation
    accounts = db.accounts.find()
    for i in accounts:
        print(i)


def get_account_info(id):
    obj_id = ObjectId(id)
    client = MongoClient(config["mongodb"]["host"], int(config["mongodb"]["port"]))
    db = client.planetaryVegetation
    account = db.accounts.find_one({"_id": obj_id})
    return account


def usage():
    output = """
    Usage:
        twitter_automation.py [list_accounts] 
        
        twitter_automation.py [add_account] [account fields ....]
        
        twitter_automation.py [stats] [_id]    # show followers and friends, live query twitter account
                                               # _id is the id from the account collection 
                                               
        twitter_automation.py [stats_db] [_id] # show followers and friends, query DB, more info and stats
                                               # _id is the id from the account collection                                                                           
                                               
        twitter_automation.py [log_stats] [_id] # count followers/friends from DB, log them to a DB time series table
                                                # _id is the id from the account collection
                                                
        twitter_automation.py [show_logged_stats] [_id] # show stats from DB time series for this account
                                               # _id is the id from the account collection                                                                          
        
        twitter_automation.py [store] [_id]    # store existing followers and friends
                                               # _id is the id from the account collection 
              
        twitter_automation.py [unfollow] [_id] # SLOWLY unfollow - use with caution
                                               # _id is the id from the account collection
                                               
        twitter_automation.py [find_friends] [_id] [keyword]  # find friends based on keyword
                                                              # _id is the id from the account collection
                                                     
        twitter_automation.py [auto_follow] [_id] [keyword]  # same as find friends except that it actually follows them
                                                             # _id is the id from the account collection                                                         
                                               
        
        
        - watch out for special characters, you probably don't want to do this from the CLI
                
        Account fields:
                 username
                 password
                 email
                 fname
                 lname
                 vertical
                 notes
                 consumerKey
                 consumerSecret
                 accessToken
                 accessTokenSecret
        """
    print output


if __name__ == "__main__":

    load_configs()

    if len(sys.argv) == 13:

        if sys.argv[1] == "add_account":
            add_account(sys.argv[2:])
        else:
            usage()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "list_accounts":
            list_accounts()

    elif len(sys.argv) == 3:
        if sys.argv[1] == "stats":
            account = get_account_info(sys.argv[2])
            twitter1 = auth(account)
            data = get_stats(twitter1, account)
            print("followers: " + str(data[0]))
            print("friends: " + str(data[1]))
        elif sys.argv[1] == "stats_db":
            account = get_account_info(sys.argv[2])
            data = get_stats_db(account)
            print("friends: " + str(data[0]))
            print("followers: " + str(data[1]))
            print("follow backs: " + str(data[2]))
            print("friends not following: " + str(data[3]))
        elif sys.argv[1] == "log_stats":
            account = get_account_info(sys.argv[2])
            log_stats_to_db(account)

        elif sys.argv[1] == "show_logged_stats":
            account = get_account_info(sys.argv[2])
            data = show_logged_stats(account)
            for i in data:
                print(i)

        elif sys.argv[1] == "store":
            account = get_account_info(sys.argv[2])
            twitter1 = auth(account)
            store_existing_users(twitter1, account)

        elif sys.argv[1] == "unfollow":
            account = get_account_info(sys.argv[2])
            twitter1 = auth(account)
            unfollow(account, twitter1)

        else:
            usage()
    elif len(sys.argv) == 4:
        if sys.argv[1] == "find_friends":
            account = get_account_info(sys.argv[2])
            twitter1 = auth(account)
            find_friends(account, twitter1, sys.argv[3])
        elif sys.argv[1] == "auto_follow":
            account = get_account_info(sys.argv[2])
            twitter1 = auth(account)
            auto_follow(account, twitter1, sys.argv[3])
        else:
            usage()
    else:
        usage()

        """
    
        if sys.argv[1] == "update":
            results = load_db_all()
            print results

        if sys.argv[1] == "get-feeds":
            twitter1 = auth("xxxxxxxx")
            fs = FeedSource.FeedSource(twitterobj=twitter1, social_media_type="twitter", feed_topic="tech", user="xxxxxxxxxxxx", maxRuns=1, sleepTimeP=30)
            fs.getFeeds()

        if sys.argv[1] == "run-feeds":
            twitter1 = auth("xxxxxxxxx")
            fs = FeedSource.FeedSource(twitterobj=twitter1, social_media_type="twitter", feed_topic="tech", user="xxxxxxxxxxxx", maxRuns=50, sleepTimeP=14400)  # every 2 hours - 14400
            fs.runFeed()
        """


