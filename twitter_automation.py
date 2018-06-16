
import sys
import os
import subprocess
from twitter import *
import time
import datetime
import json
import sys
import os
import twitter_util
import FeedSource
sys.path.append(os.path.abspath("/home/user1/Desktop"))
import boulder_valley     



"""
def showMetricsFromDB():
    cursor.execute("SELECT twitter_metrics.date, twitter_accounts.first_name, twitter_accounts.last_name, twitter_metrics.following, twitter_metrics.followers, twitter_metrics.tweets  from twitter_accounts LEFT JOIN twitter_metrics ON twitter_metrics.twitter_acct=twitter_accounts.ID ")
    print( "date, name, follwing, followers, tweets")
    for i in cursor:
        print i

"""

def readCreds():
    f = open('./creds/creds.json', 'r')      # read them in from saved status file
    data = f.read()
    creds = json.loads(data)
    f.close()
    return creds


def auth(user=""):
    creds = readCreds()
    CONSUMER_SECRET = creds[user]["CONSUMER_SECRET"]
    CONSUMER_KEY = creds[user]["CONSUMER_KEY"]

    if not os.path.exists('./creds'):
        os.mkdir('./creds')

    MY_TWITTER_CREDS = os.path.expanduser('./creds/' + user + '.token')
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("My App Namexxx", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
    twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
    return twitter


def getStats(twitterObj,user=""):
    followers = twitter_util.getFollowers(user=user, twitterObj=twitterObj)
    friends = twitter_util.getFriends(user=user, twitterObj=twitterObj)
    return followers, friends


def autoFollow(twitterObj,user=""):
    followers, friends = getStats(twitterObj, user)
    for f1 in followers:
        if f1 not in friends:
            print f1
            twitterObj.friendships.create(user_id=f1, follow="true")
            time.sleep(67)


def getFollowers(twitterObj, user="" ):
    followers = twitterObj.followers.ids(screen_name=user)      #GET followers/ids     # get followers
    if followers["next_cursor"] != 0:
        print "\n\n\n\nWARNING - more followers exist, update code to handle these\n\n\n\n"
    return followers["ids"]


def getFriends(twitterObj, user=""):
    friends = twitterObj.friends.ids(screen_name=user)      #GET friends/ids     # get friends
    if friends["next_cursor"] != 0:
        print "\n\n\n\nWARNING - more friends exist, update code to handle these\n\n\n\n"
    return friends["ids"]


def load_db(twitter_user, twitter_id):
    auth_object1 = auth(user=twitter_user)             # get auth object for this user
    followers, friends = getStats(auth_object1, twitter_user)
    #print twitter_user + "    Followers: " + str(len(followers)) + "       Friends: " + str(len(friends))
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


def plot_data(data_file, graph_outpout_file, start_date, stop_date ):
    gnuplot_script = ' '.join((
    "set title \"Followers over time\"\n",
    "set xlabel \"Date / Time\"\n",
    "set ylabel \"Followers\"\n",
    "set term png\n",
    "set output \"" + graph_outpout_file + "\"\n", 
    "set xdata time\n",
    "set timefmt \"%Y-%m-%d %H:%M:%S\"\n",
    "set format x \"%m-%d\"\n", 
    "set xrange [\"" + start_date + "\":\"" + stop_date + "\"] \n", 
    "set datafile separator \",\"\n",
    "set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb\"#483D8B\" behind\n",  
    "plot '" + data_file + "' using 1:2 with lines linecolor rgb \"#00FF00\" \n" 
    ))
    f = open('gnuplot_script_tmp.txt', 'w')
    f.write(gnuplot_script)
    f.close()
    p = subprocess.Popen("gnuplot gnuplot_script_tmp.txt", shell = True)
    os.waitpid(p.pid, 0)
    os.remove('gnuplot_script_tmp.txt')


def graph_followers(data_file, report_file, graph_outpout_file, acct_id):
    cursor.execute("SELECT twitter_metrics.date, twitter_accounts.first_name, twitter_accounts.last_name, twitter_metrics.following, twitter_metrics.followers from twitter_accounts LEFT JOIN twitter_metrics ON twitter_metrics.twitter_acct=twitter_accounts.ID where twitter_accounts.ID=" + str(acct_id))
    results = []
    f = open(data_file, 'w')
    for i in cursor:
        results.append(i)
        f.write(str(i[0]) + "," + i[4] + "\n")
    f.close()
    f = open(report_file, 'a')
    f.write( "<h1>" + results[-1][1] + " " + results[-1][2] + "</h1>" )
    f.write( "Following: " + results[-1][3] + "<br>")
    f.write( "Followers: <b>" + results[-1][4] + "</b><br>" )
    f.write( "<img src=\"" + graph_outpout_file + "\" >" )
    f.close()
        

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



