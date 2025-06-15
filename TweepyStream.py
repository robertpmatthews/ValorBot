from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy
import MongoDB
import re
import Credentials
import urllib3
import requests
from time import sleep
from http.client import IncompleteRead as http_incompleteRead
# # # # TWITTER STREAM LISTENER # # # #


class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        try:
            id_str = re.search('id_str":"(.+?)"', data).group(1)
            screen_name = re.search('"screen_name":"(.+?)"', data).group(1)
            if screen_name == 'riotgames':
                url = "https://twitter.com/" + screen_name + "/status/" + id_str
                MongoDB.insert_url(url, screen_name)
            if screen_name == 'PlayVALORANT':
                url = "https://twitter.com/" + screen_name + "/status/" + id_str
                MongoDB.insert_url(url, screen_name)
            if screen_name == 'LeagueOfLegends':
                url = "https://twitter.com/" + screen_name + "/status/" + id_str
                MongoDB.insert_url(url, screen_name)
            if screen_name == 'TFT':
                url = "https://twitter.com/" + screen_name + "/status/" + id_str
                MongoDB.insert_url(url, screen_name)
            if screen_name == 'PlayRuneterra':
                url = "https://twitter.com/" + screen_name + "/status/" + id_str
                MongoDB.insert_url(url, screen_name)
            if screen_name == 'CoSlobby':
                url = "https://twitter.com/" + screen_name + "/status/" + id_str
                MongoDB.insert_url(url, screen_name)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        if status == 420:
            return False
        return True


class MyStream:

    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self, twitid):
        try:
            self.stream.filter(follow=twitid,stall_warnings=True)
        except http_incompleteRead as error:
            print(error)
            sleep(5)
        except urllib3.exceptions.ProtocolError as error:
            print(error)
            sleep(5)
        except ConnectionResetError as error:
            print(error)
            sleep(5)
        except ConnectionError as error:
            print(error)
            sleep(5)
        except requests.exceptions.ConnectionError as error:
            print(error)
            sleep(5)
        except Exception as error:
            print("Hm didn't know about that one " + str(error))
            sleep(5)


streaming = True
while streaming:
    print("running")
    # Authenticate using config.py and connect to Twitter Streaming API.
    twitid = ["20523846", "577401044", "1230550898616586242", "1129499230840578048", "1052681244910092288",
              "1262900617799966722"]
    # list of id Riot, LoL, Valorant, TFT, LoR, coSlobby

    # This handles Twitter authentication and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(Credentials.Consumer_Key, Credentials.Consumer_Secret)
    auth.set_access_token(Credentials.Access_Token, Credentials.Access_Token_Secret)
    stream = MyStream(auth, listener)
    stream.start(twitid)
