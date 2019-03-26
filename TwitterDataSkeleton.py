import codecs
import json
from simplemapplot import make_us_state_map

stateAbbrevList = ["AK","AL","AR","AZ","CA","CO","CT","DE",
                   "FL","GA","HI","IA","ID", "IL","IN","KS",
                   "KY","LA","MA","MD","ME","MI","MN","MO",
                   "MS","MT","NC","ND","NE","NH","NJ","NM",
                   "NV","NY", "OH","OK","OR","PA","RI","SC",
                   "SD","TN","TX","UT","VA", "VT", "WA","WI",
                   "WV","WY"]

SENTIMENTCOLORS = ["#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#bababa", "#fee090", "#fdae61", "#f46d43", "#d73027"]

def parseTweet(line):
    ''' str -> list
    PRE:  takes a string that is one tweet with metadata
    POST: returns a list extracting several fields from the tweet
          ordered as: [0] date, [1] id, [2] text of tweet,
          [3] number of followers,[4] number of friends, [5] country,
          [6] city, state.  Note the last field is a single string
          with the city name followed by a comma by the state abbrev.
    '''
    tweet = json.loads(line)
    date = tweet['created_at']
    id = tweet['id']
    numFollowers = tweet['user']['followers_count']
    numFriends = tweet['user']['friends_count']
    country = tweet['place']['country_code']
    cityState = tweet['place']['full_name']

    if 'retweeted_status' in tweet:
    	text = tweet['retweeted_status']['text']
    else:
    	text = tweet['text']
    	
    return [date, id, text, numFollowers, numFriends, country, cityState]


def readTweetFile(tList, filename):
    '''list, str -> void
    This function takes in a list and the filename of a json file of tweets.
    It reads the json file line by line and extracts some fields from that
    file and puts combines those fields into a list and appends the list to tList.  
    '''

    tweetFile = codecs.open(filename, 'r', 'utf-8')
    for line in tweetFile:
        try:
            item = parseTweet(line)
            if item[5] == "US" and item[6][-2:] in stateAbbrevList:
                tList.append(item)
                #print(tweetList[-1])  #Uncomment this line of code if you want to see the list of valid tweets.
                                       #This can be helpful when you're working with the sandwich.json file but
                                       #definitely not helpful when you're working with the large data files!
        except:
            pass
    tweetFile.close()   



######
# MAIN
#

tweetList = []
sentimentDict = {}
stateCountDict = {}
stateSentimentScoreDict = {}

for state in stateAbbrevList:
    stateCountDict[state] = 0
    stateSentimentScoreDict[state] = 0

readTweetFile(tweetList,"sandwich.json") 

#
# Your main program code goes here
#

#make_us_state_map(stateSentimentScoreDict, SENTIMENTCOLORS)






