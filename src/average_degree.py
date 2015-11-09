import json, sys

source = open(sys.argv[1], 'r')
dest = open(sys.argv[2], 'w')

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
        dest.write("Avg: " + str(getAverage(edges, vertices)) + "\n")
    source.close()
    dest.close()

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

def getAverage(edges, vertices):
    return round(2 * (float(edges) / float(vertices)),2) if (vertices > 0) else 0.00

def getSeconds(timestamp):
    ts = timestamp.split(' ')
    nums = ts[3].split(':')
    return (int(nums[0])*60*60) + (int(nums[1])*60) + (int(nums[2]))

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

def _prune(graph, hashtags, edges, vertices):
    for first in xrange(0,len(hashtags)-1):
        for second in xrange(first+1,len(hashtags)):
            graph[hashtags[first]].remove(hashtags[second])
            graph[hashtags[second]].remove(hashtags[first])
            edges -= 1
            if len(graph[hashtags[first]]) == 0:
                graph.remove(hashtags[first])
                vertices -= 1
            if len(graph[hashtags[second]]) == 0:
                graph.remove(hashtags[second])
                vertices -= 1
    return [edges,vertices]

if __name__ == "__main__":
    main()


# to do:
# sanitize hashtags, ignore
# pairify
# calculate average
