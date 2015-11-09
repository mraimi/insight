Michael Raimi
mar2260@columbia.edu

Written and tested on python 2.7.6

A high level description of my solutions:

First Feature:

There's not much cleverness or design in feature 1 aside from
how I keep count of tweets with unicode characters. By assuming the string 
is valid ascii and catching the exceptions that result when processing
unicode characters I know how many tweets contained unicode. 
This was inspired by the following:

(http://stackoverflow.com/questions/1207457/convert-a-unicode-string-to-a-string-in-python-containing-extra-symbols)

Second Feature:

Data structures:
I used two main data structures for this feature. Firstly to represent the actual graph I decided to use
a python dictionary to create an adjacency list. This results in constant time lookup for
the existance of a vertex in the graph but a to lookup whether two vertices are connected results
in a lookup linear in the number of vertices.

In retrospect I may have opted to create a dictionary of dictionaries for better lookup times.
This would allow constant existance lookup (whether a vertex is in the graph) as well as constant 
connectedness lookup (whether two vertices are connected.) Insertion and deletion would be constant
as well. The memory overhead of many potentially huge hash tables is a concern I would have
with this approach though.

The second data structure is a list of lists. I chose this data structure because I wanted
it to maintain ordered records of tweets in the current 60 second window. It prunes tweets
by going from the front of the list (oldest tweets) until it finds the first tweet that is 
recent enough to hang around. It short circuits in that it may not need to go through all
the records. If I could refactor this code I would only generate the hashtag pairs once since
it's a quadratic runtime operation. However, I deemed this non-essential as it doesn't affect
the overall big-O complexity of the code.


This code challenge was really fun! Thanks for taking the time to review my submission!







