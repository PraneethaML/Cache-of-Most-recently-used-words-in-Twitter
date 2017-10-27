from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#Variables that contains the user credentials to access Twitter API 
access_token = "1322512952-13U0KQWflirRj9TGzwjQeEMpsi8N9vbY7aYyNP5"
access_token_secret = "T7dQcdOsgWhdaoxNnvT6ZjACe5QI0QZD3ULyRUaZJDCrq"
consumer_key = "pCe5mSXcFrO37P8qUyHFTJn2h"
consumer_secret = "wt6Jp8rrh6jdDbV1AlpTikl2guYoVUe8bBVST8q9UdvCwZzeZC"

# Take user input for keyword
var = raw_input("Please enter keyword: ")
print "you entered", var


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        
        return True
 
    def on_error(self, status):
        print(status)
        return True
    
if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    
stream.filter(track=[var])