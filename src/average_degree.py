import json, sys

source = open(sys.argv[1], 'r')
dest = open(sys.argv[2], 'w')

for line in source:
    jl = json.loads(line)
    if 'entities' in jl:
        if 'hashtags' in jl['entities']:
            for ht in jl['entities']['hashtags']:
                if 'text' in ht:
                    dest.write(ht['text'].encode('ascii','ignore')+' ');
            dest.write('\n')
source.close()
dest.close()
