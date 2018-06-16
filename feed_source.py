

# feed list needs to be configurable, new one for every verticle
# need better feeds
# need a blacklist file on disk of stuff not to repost ( save "feeds_done" array to disk )
# specify sleep time and max per run as params from interface
# all data files in a data subdir
# test with multiple verticles    ( should be ready for this )  make it easier to configure
# view running and waiting jobs
# better job control
# proceedure for new verticles
# params that make sense in place for each verticle  ( some kind of interface with saved params )





import feedparser
import json
import time
from twitter import *
import os
import sys
#import pytumblr

class FeedSource:

    #sleepTime = 15   # 5 mins
    sleepTime = 600   # 5 mins
    maxPerRun = 25
    feed_list = {"android_game": ["http://www.reddit.com/r/Games/.rss", "http://www.reddit.com/r/AndroidGaming/.rss"],
                 "tech": ["https://www.reddit.com/r/Ubuntu/.rss", "https://www.reddit.com/r/mongodb/.rss", "https://www.reddit.com/r/mysql/.rss", "https://www.reddit.com/r/ansible/.rss"]}

    twitterobj_i = None
    user_i = None


    def __init__(self, twitterobj=None, tumbler_object=None, tumbler_blog=None, social_media_type="", feed_topic="", user="", maxRuns="1",sleepTimeP=600):
        pass
        self.twitterobj_i = twitterobj
        self.tumbler_object = tumbler_object
        self.tumbler_blog = tumbler_blog
        self.user_i = user
        self.maxPerRun = maxRuns
        self.sleepTime=sleepTimeP
        self.social_media_type = social_media_type
        self.feed_topic = feed_topic
        self.feeds = self.feed_list[self.feed_topic]


    def tweetMyText(self, tweet="fail"):
        """
        - needs to be authenticated first
        - pass text with tweet variable, it will be tweeted
        """
        print("tweet ~")
        if tweet != "fail":
            try:
                self.twitterobj_i.statuses.update(status=tweet)
            except:
                print "ERROR Tweeting"

    """
    # no tumblr for now .....
    def tumbleMyText(self, tumble="fail"):
        print("tumble ~")
        if tumble != "fail":
            try:
                self.tumbler_object.create_text(self.tumbler_blog, state="published", title="", body=tumble)
            except:
                print  "ERROR Tumbling"
    """

    def getFeeds(self):
        """
            - pulls in feed data, based on global list
            - stores in a json file
        """
        feedData1 = []         # actual feed data
        feedsDone = []         # completedd feeds already tweeted
        for i in self.feeds:
            d = feedparser.parse(i)
            for post in d.entries:
                #print post.title + "\n" + post.description + "\n" + post.link + "\n"
                feedData1.append(post.title + "\n" + post.link + "\n")
        f = open('data/feed_job_' + self.feed_topic + "_" + self.social_media_type + "_" + self.user_i, 'w')
        f.write(json.dumps([feedsDone, feedData1]))
        f.close()

    def runFeed(self):
        """
            - reads json file for send and pending tweets
            - sends those out, updates the list
        """
        print "\n\n=================================="
        print "Running feeds for: " + self.user_i
        f = open('data/feed_job_' + self.feed_topic + "_" + self.social_media_type + "_" + self.user_i, 'r')      # read them in from saved status file
        data = f.read()                # friends that are already done
        f.close()
        feedsDone, feedData1 = json.loads(data)
        tmp = feedData1[:]
        counter = 0
        for i in tmp:
            counter += 1
            print str(counter) + " of " + str(self.maxPerRun)
            if len(i) < 140:                  # trim if too big for twitter
                trimmed = i[0:138]
            else:
                trimmed = i
            if self.social_media_type == "twitter":
                self.tweetMyText(trimmed)
            elif self.social_media_type == "tumblr":
                self.tumbleMyText(trimmed)
            else:
                print "ERROR - no social media type specified"
                exit(1)
            feedsDone.append(i)
            feedData1.remove(i)
            time.sleep(self.sleepTime)
            if counter > self.maxPerRun:
                break
        f = open('data/feed_job_' + self.feed_topic + "_" + self.social_media_type + "_" + self.user_i, 'w')
        f.write(json.dumps([feedsDone, feedData1]))
        f.close()
        print "Feed run stats:"
        print "-----------------"
        print "Pending: " + str(len(feedData1))
        print "Done:    " + str(len(feedsDone))




