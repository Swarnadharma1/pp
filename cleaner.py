
import pandas as pd
import re #regular expression
import string
#                   Explaination of Above modules

#  import pandas as pd:
#  Used for reading,writing and extraction of all Kinds of Spreadsheet.
#  One of the most used Data Scientist Tools.
# 
#  import re:
#  re -> Regular Expression. Most of the hard work is done with this.
#
#  import string:
#  Contains many string based functions.
#
#  import preprocessor as p:
#  It is a module outsourced in Github. Used to remove hashtags from tweets.
#  Along with other stuff
class Cleaner():
    def __init__(self,verbose=False):
    #HappyEmoticons
        self.emoticons_happy = set([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
            '<3'
            ])
        self.verbose = verbose
        # Sad Emoticons
        self.emoticons_sad = set([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
            ':c', ':{', '>:\\', ';('
            ])
            #Emoji patterns
        self.emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE)
        
        #combine sad and happy emoticons
        self.emoticons = self.emoticons_happy.union(self.emoticons_sad)
    
        self.SMILEYS_PATTERN = re.compile(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}", re.IGNORECASE)
        self.NUMBERS_PATTERN = re.compile(r"(^|\s)(\-?\d+(?:\.\d)*|\d+)")
        self.URL_PATTERN=re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
        self.HASHTAG_PATTERN = re.compile(r'#\w*')
        self.MENTION_PATTERN = re.compile(r'@\w*')
        self.RESERVED_WORDS_PATTERN = re.compile(r'^(RT|FAV)')


    def fit(self, X, y=None):
        if(self.verbose):
            print("Verbose mode on!")
        return self
    # This Functions cleans all the remaining unnecessary details left by
    # "preprocessor" module
    
    def transform(self,X,y=None):
        temp = []
        for tweet in X:
            tweet = bytes(tweet, 'utf-8').decode('unicode_escape', 'ignore')
            tweet = self.URL_PATTERN.sub(r'',tweet)
            tweet = self.HASHTAG_PATTERN.sub(r'',tweet)
            tweet = self.MENTION_PATTERN.sub(r'',tweet)
            tweet = self.RESERVED_WORDS_PATTERN.sub(r'',tweet)
            tweet = self.SMILEYS_PATTERN.sub(r'',tweet)
            tweet = self.NUMBERS_PATTERN.sub(r'',tweet)
            tweet = tweet.lower()
            tweet = re.sub(r':', '', tweet)
            tweet = re.sub(r'‚Ä¶', '', tweet)
        #replace consecutive non-ASCII characters with a space
            tweet = re.sub(r'[^\x00-\x7F]+','', tweet)
            tweet = re.sub(r'[\0]+','',tweet)
            tweet = re.sub(r'[\1]+','',tweet)
        #remove emojis from tweet
            tweet = self.emoji_pattern.sub(r'', tweet)
            tweet=re.sub(r'b\'','',tweet)
            tweet=re.sub(r'b\"','',tweet)
            tweet = re.sub("&amp;",'',tweet)
            tweet = re.sub("https//",'',tweet)
            tweet = re.sub(r'[\']+','',tweet)
            tweet = re.sub(r'[`]+','',tweet)
            tweet = re.sub(r'["]+','',tweet)
            temp.append(tweet)
        
        return temp
# Read Tweets, Place them in a dataFrame, Clean all of them and place them
# in a "csv" all of them is done here 
if __name__ == "__main__":
    df = pd.read_csv("tweet/imVkohli_tweets.csv")
    data=list(df.iloc[:,2])
    stage1=[]
    for ip in data:
        stage1.append(ip)
    df = pd.read_csv("tweet/elonmusk_tweets.csv")
    data=list(df.iloc[:,2])
    for ip in data:
        stage1.append(ip)
    df = pd.read_csv("tweet/J_tsar_tweets.csv")
    data=list(df.iloc[:,2])
    for ip in data:
        stage1.append(ip)
    df = pd.read_csv("tweet/BarackObama_tweets.csv")
    data=list(df.iloc[:,2])
    for ip in data:
        stage1.append(ip)
    clean = Cleaner()
    stage2 = clean.transform(stage1)
    stage2= [" ".join(string.split()) for string in stage2]
    stage2 = [x for x in stage2 if x]
    df = pd.DataFrame(stage2, columns=["Tweet"])
    df.to_csv('person.csv',index=False)   











