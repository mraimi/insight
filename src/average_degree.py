import json, sys

source = open(sys.argv[1], 'r')
dest = open(sys.argv[2], 'w')

def main():
    edges = 0
    vertices = 0
    graph = dict()
    for line in source:
        jl = json.loads(line)
        hashtags = []
        if 'entities' in jl:
            if 'hashtags' in jl['entities']:
                for ht in jl['entities']['hashtags']:
                    if 'text' in ht:
                        hashtags.append(ht['text'].encode('ascii','ignore').lower());
        print str(hashtags)
        newVals = pairify(hashtags, graph, edges, vertices)
        edges = newVals[0]
        vertices = newVals[1]
        dest.write("Avg: " + str(getAverage(edges, vertices)) + "\n")
    source.close()
    dest.close()

def pairify(hashtags, graph, edges, vertices):
    for first in xrange(0,len(hashtags)-1):
        for second in xrange(first+1,len(hashtags)):
            if hashtags[first] not in graph:
                vertices += 1
                edges += 1
                if hashtags[second] not in graph:
                    vertices += 1
                    graph[hashtags[first]] = [hashtags[second]]
                    graph[hashtags[second]] = [hashtags[first]]
                else:
                    graph[hashtags[first]] = [hashtags[second]]
                    graph[hashtags[second]].append(hashtags[first])
            elif hashtags[first] in graph:
                if hashtags[second] not in graph:
                    vertices += 1
                    edges += 1
                    graph[hashtags[first]].append(hashtags[second])
                    graph[hashtags[second]] = [hashtags[first]]
                elif hashtags[second] not in graph[hashtags[first]]:
                    graph[hashtags[first]].append(hashtags[second])
                    graph[hashtags[second]].append(hashtags[first])
    return [edges,vertices]

def getAverage(edges, vertices):
    return 2 * (float(edges) / float(vertices)) if (vertices > 0) else 0

if __name__ == "__main__":
    main()


# to do:
# sanitize hashtags, ignore
# pairify
# calculate average
