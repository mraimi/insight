import json

source = open('../data-gen/tweets.txt', 'r')
dest = open('../tweet_output/ft1.txt','w')
unicodeCount = 0
for line in source:
    text = ''
    created = ''
    jl = json.loads(line)
    if 'text' in jl:
        s = jl['text']
        text = s.encode('ascii','ignore')
        text = text.replace('\n',' ').replace('\t',' ')

        # Determines whether a tweet has unicode by assuming it's ascii.
        # If an encode error is thrown that means the string contained
        # some unicode at which point we bump the unicode counter.
        try:
            s.decode('ascii')
        except UnicodeEncodeError:
            unicodeCount += 1
    if 'created_at' in jl:
        created = jl['created_at']
    dest.write(text + ' (timestamp: ' + created + ')\n')
dest.write('\n'+ str(unicodeCount) + ' tweet(s) contained unicode.\n')
source.close()
dest.close()