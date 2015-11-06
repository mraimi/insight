# example of program that calculates the number of tweets cleaned
import json

source = open('/home/hadoop/Documents/dev/insight/coding-challenge/data-gen/tweets.txt', 'r')
dest = open('/home/hadoop/Documents/dev/insight/coding-challenge/tweet_output/ft1.txt','w')
unicodeCount = 0
for line in source:
    jl = json.loads(line)
    if 'text' in jl:
        s = jl['text']
        clean = s.encode('ascii','ignore')
        clean = clean.replace('\n',' ').replace('\t',' ')
        if (len(clean) > 0):
            dest.write(clean+'\n')
        try:
            s.decode('ascii')
        except UnicodeEncodeError:
            unicodeCount += 1
dest.write('\n'+ str(unicodeCount) + ' tweet(s) contained unicode.\n')