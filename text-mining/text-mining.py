#!/usr/bin/python

#import the necessary modules
import sys
import pymongo
import json
import ConfigParser

#import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class StdOutListener(StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()

        self.db = pymongo.MongoClient().test #change test to prod db name

    ''' This is a basic listener that just prints received tweets to stdout. '''
    def on_data(self, data):
        self.db.tweets.insert(json.loads(data)) #saves data in tweets collection

        #debug print
        print "Entry saved in db. There are " + str(self.db.tweets.count()) + " entries in the collection."
        return True

    def on_error(self, status):
        print status
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream

class Utils:
    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    print "skip: %s" % option
            except:
                print "exception on %s!" % option
                dict1[option] = None
        return dict1

if __name__ == '__main__':
    try:
        with open('./conf.ini'):
            config = ConfigParser.ConfigParser()
            config.read('./conf.ini')
    except:
        raise ValueError("no config.ini file found - try looking into _config.ini")

    consumer_key = Utils.config_section_map('ApiSetup')['api_key']
    consumer_secret = Utils.config_section_map('ApiSetup')['api_secret']
    access_token = Utils.config_section_map('ApiSetup')['access_token_key']
    access_token_secret = Utils.config_section_map('ApiSetup')['access_token_secret']

    #This handles Twitter authetification and the connection to Twitter Streaming API
    outListener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, outListener)
    if len(sys.argv) <= 1:
        raise ValueError("exception: no argument found - use 'python text-mining.py arg1...'")
    else:
        stream.filter(track=sys.argv[1:])
