import json, sys, datetime, time

source = open(sys.argv[1], 'r')
dest = open(sys.argv[2], 'w')

# We do our bookkeeping through two main data structures - 
# a dictionary of lists is used to create an adjacency list
# giving O(1) access to see whether a vertex
# exists in the graph. An ordered list keeps track of our
# current window of valid tweets. NOTE: testing whether
# a vertex is directly connected to another vertex is linear in the 
# number of vertices in the graph as a single node may be 
# connected to all other nodes, resulting in a long list
def main():
    edges = 0
    vertices = 0
    graph = dict()
    ordered = []
    created = None
    
    for line in source:
        jl = json.loads(line)
        if 'limit' in jl:
            continue
        hashtags = []
        if 'entities' in jl:
            if 'hashtags' in jl['entities']:
                for ht in jl['entities']['hashtags']:
                    if 'text' in ht:
                        hashtags.append(ht['text'].encode('ascii','ignore').lower());
        created = jl['created_at']
        if 'created_at' in jl:
            ordered.append([created] + hashtags)
        postPruneVals = prune(jl['created_at'],edges,vertices,ordered,graph)
        newVals = pairify(hashtags, graph, postPruneVals[0], postPruneVals[1])
        edges = newVals[0]
        vertices = newVals[1]
        dest.write("{0:.2f}".format(getAverage(edges, vertices)) + "\n")
    
    source.close()
    dest.close()

# This function creates all pairings from a list of
# hashtags. It is quadratic in complexity
def pairify(hashtags, graph, edges, vertices):
    
    for first in xrange(0,len(hashtags)-1):
        for second in xrange(first+1,len(hashtags)):
            if hashtags[first] not in graph:
                edges += 1
                if hashtags[second] not in graph:
                    if hashtags[first] != hashtags[second]:
                        vertices += 2
                        graph[hashtags[first]] = [hashtags[second]]
                        graph[hashtags[second]] = [hashtags[first]]
                else:
                    vertices += 1
                    graph[hashtags[first]] = [hashtags[second]]
                    graph[hashtags[second]].append(hashtags[first])
            elif hashtags[first] in graph:
                if hashtags[second] not in graph:
                    vertices += 1
                    edges += 1
                    graph[hashtags[first]].append(hashtags[second])
                    graph[hashtags[second]] = [hashtags[first]]
                elif hashtags[second] not in graph[hashtags[first]]:
                    if hashtags[first] != hashtags[second]: 
                        edges += 1
                        graph[hashtags[first]].append(hashtags[second])
                        graph[hashtags[second]].append(hashtags[first])

    return [edges,vertices]

# In graph theory this is a well known formula to calculate
# the average degree of an undirected graph
def getAverage(edges, vertices):

    return round(2 * (float(edges) / float(vertices)),2) if (vertices > 0) else 0.00

# Converts twitter timestamps into datetime objects
# which are then converted to epoch time
def getSeconds(timestamp):
    dt = datetime.datetime.strptime(timestamp, "%a %b %d %H:%S:%M +0000 %Y")
    seconds = time.mktime(dt.timetuple())

    return seconds

# Goes through the ordered lists to find which tweets should be pruned.
# This function short-circuits as soon as it finds a tweet that is
# recent enough. It assumes that the tweets are in chronological
# order from oldest to new.
def prune(timestamp, edges, vertices, ordered, graph):
    cpy = ordered[:]
    for record in cpy:
        if getSeconds(timestamp) - getSeconds(record[0]) > 60:
            newVals = _prune(graph, record[1:], edges, vertices)
            edges = newVals[0]
            vertices = newVals[1]
            ordered.remove(record)
        else:
            return [edges, vertices]

    return [edges,vertices]

# Helper function that actually does the modifying of the data structures
# and counts
def _prune(graph, hashtags, edges, vertices):

    for first in xrange(0,len(hashtags)-1):
        for second in xrange(first+1,len(hashtags)):
            if second in hashtags and hashtags[second] in graph[hashtags[first]]:
                graph[hashtags[first]].remove(hashtags[second])
                edges -= 1
            if first in hashtags and hashtags[first] in graph[hashtags[second]]:
                graph[hashtags[second]].remove(hashtags[first])
            if len(graph[hashtags[first]]) == 0:
                del graph[hashtags[first]]
                vertices -= 1
            if len(graph[hashtags[second]]) == 0:
                del graph[hashtags[second]]
                vertices -= 1
    
    return [edges,vertices]

if __name__ == "__main__":
    main()
