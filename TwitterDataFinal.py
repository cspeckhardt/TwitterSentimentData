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

###### Read Sentiment File #############
    
def readSentimentFile(sList, filename):
    '''
    PRE: The sentiment list and filename are passed to this function
    POST: The function returns the full Sentiment Dictionary
    We open the file 'filename' and read through it line by line. We split
    at commas and save each piece of data into the new dictionary.
    '''
    fullSentimentDict= {}
    SentimentFile= open(filename, "r")
    for line in SentimentFile:

        line=line.strip()
        
        data= line.split(",")

        fullSentimentDict[data[0]]= float(data[1])

    SentimentFile.close()

    return fullSentimentDict



############ find Min ###################



def findMin (ScoreDict):

    '''
    PRE:input is the score dictionary
    POST:outputs the minimum value of the score dictionary
    This function uses the built in min function to find the
    minimum value of the ScoreDict values.
    '''
    
    minimum=min(ScoreDict.values())

    return minimum

########## find Max ##############


def findMax (ScoreDict):
    
    '''
    PRE:input is the score dictionary
    POST:outputs the maximum value of the score dictionary
    This function uses the built in max function to find the
    maximum value of the ScoreDict values.
    '''
    maxium=max(ScoreDict.values())

    return maxium

############ Assign Colors ############

def assignColor(ST, ScoreDict, Max, Min):
    '''
    PRE: The state, score dictionary, and max and min are
    passed to the function
    POST: The ScoreDict[ST] is returned containing the color value
    instead of the sentiment score.
    We use a series of if statements to create parameters for the
    assignments of colors. Each color represents a certain percentage of
    the minimum and maximum scores.
    '''
    if ScoreDict[ST]== 0:
        
        ScoreDict[ST]= 4

    elif ScoreDict[ST]< 0:
        
        if ScoreDict[ST] <0.6*Min:
        
            ScoreDict[ST]= 0
        
        elif ScoreDict[ST]< 0.3*Min:
        
            ScoreDict[ST]= 1
        
        elif ScoreDict[ST]< 0.15*Min:

            ScoreDict[ST]= 2
        
        elif ScoreDict[ST]< 0:

            ScoreDict[ST]= 3

    elif ScoreDict[ST]> 0:
        
        if ScoreDict[ST]> 0.6*Max:

            ScoreDict[ST]=8
        
        elif ScoreDict[ST]> 0.3*Max:

            ScoreDict[ST]= 7
        
        elif ScoreDict[ST]> 0.15*Max:

            ScoreDict[ST]= 6
        
        elif ScoreDict[ST]> 0:

            ScoreDict[ST]= 5


    return ScoreDict[ST]
  
####################
        
# MAIN
#
sentimentList=[]
tweetList = []
sentimentDict = {}
stateCountDict = {}
stateSentimentScoreDict = {}
j=0
listOfScores=[]
for state in stateAbbrevList:
    stateCountDict[state] = 0
    stateSentimentScoreDict[state] = 0
    
readTweetFile(tweetList,"usaTweetsFeb19.json")
readTweetFile(tweetList,"usaTweetsFeb25.json")
fullDict= readSentimentFile (sentimentList, "sentimentsFull.csv")

interest= input("What is your word of interest? ")

######## enter a specific tweet ##########

for tweet in tweetList:
    
    st= tweet[6][-2:]
    y= tweet[2]

    tweetLower= y.lower()

   # print("Text of the tweet is ",tweetLower)
    

###### State Count #######

    if interest in tweetLower:

        stateCountDict[st] = stateCountDict[st] + 1
            

####### Raw Sentiment Score #########

            
        for sent in fullDict:
        
            if sent in tweetLower:

                stateSentimentScoreDict[st]= stateSentimentScoreDict[st]+ fullDict[sent]

            
########## Average Sentiment Score ###########
            
for State in stateCountDict:

    if stateCountDict[State]!= 0:
        
        stateSentimentScoreDict[State]= (stateSentimentScoreDict[State]/stateCountDict[State])

    #print(State, stateCountDict[State], stateSentimentScoreDict[State])
        
for state in stateAbbrevList:
    print( state, "\n" "state score: ", stateSentimentScoreDict[state], "\n" "state count: " , stateCountDict[state])
            
########### Color Assignment ##############

minimum= findMin(stateSentimentScoreDict)
maximum= findMax(stateSentimentScoreDict)

for ST in stateSentimentScoreDict:

    stateSentimentScoreDict[ST]= assignColor(ST, stateSentimentScoreDict, maximum, minimum)


make_us_state_map(stateSentimentScoreDict, SENTIMENTCOLORS)






