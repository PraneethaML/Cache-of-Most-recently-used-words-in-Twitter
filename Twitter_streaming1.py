from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import time


#Variables that contains the user credentials to access Twitter API 
access_token = "1322512952-13U0KQWflirRj9TGzwjQeEMpsi8N9vbY7aYyNP5"
access_token_secret = "T7dQcdOsgWhdaoxNnvT6ZjACe5QI0QZD3ULyRUaZJDCrq"
consumer_key = "pCe5mSXcFrO37P8qUyHFTJn2h"
consumer_secret = "wt6Jp8rrh6jdDbV1AlpTikl2guYoVUe8bBVST8q9UdvCwZzeZC"

# Take user input for keyword
var = raw_input("Please enter keyword: ")
print "you entered", var

words = {}
time1 = time.time()	#start time
time2 = time1
N = 100			#max size of cache
flag = 0			#flag to output every 1 minute



#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    def score(self):						#this function updates count of each word
    					
    		if len(words) > 0:					#do not look into dictionary if empty
    			keys = words.keys()			#list of keys to be updated
    			for key in keys:
    				if(time2 - words[key][1] >= 60):	#decrease the score if older than 60 sec
    					words[key][0] = words[key][0] - 1
    					if(words[key][0] < 0):			#delete  if score < 0
    						del words[key]
    
    def process_data(self, data):				#this function processes twitter data
    		global time1
    		global time2
    		global flag
    		list_words = data.split()				#list of words in data	
    		length = len(words)

    		for word in list_words:					#these are the words to be inserted in dictionary
    			if(time.time() - time1 >= 30):
    				break
    			if length == N:						#if dictionary reaches its size
    				key = words.keys()			#list of present keys in dictionary
    				for entry in key:				#delete entry with 0 score
    					if(words[entry][0] == 0):
    						del words[entry]
    				length = len(words)
    				if(length == N):				#if size of dictionary does not reduce
    					break						#then do not add any more words

    			if(word in words):				#if word is already present then update its score
    				words[word][0] = words[word][0] + 1
    				words[word][1] = time.time() #Note time when entry is updated
    			else:								#else word is new. Insert it in dictionary
    				words[word] = [1, time.time()]	#Note time when entry is inserted
    				length = length + 1				#use this time later to determine age of entry

    		if(time.time() - time1 >= 30):			#update dictionary every 30 sec
    			time1 = time.time()
    			time2 = time1
    			flag = flag + 1
    			self.score()
    			if(len(words) > 0 and flag == 2): #flag = 2 => 60 seconds passed
    				for keys in words:			#print words in dictionary 
    					if(words[keys][0] > 1):
    						print keys, words[keys][0]
    				flag = 0	#update flag to print on every 60 sec
    				print 'wait for 1 minute to get words in cache'
    

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if("text" in data):				#if there is any tweet data, its key will be 'text'
        	data1 = [data["text"]]		#extract tweet from tons of data
        else:							#else go for next tweet data
        	return(True)
        
        self.process_data(data1[0])
        return(True) 
        
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