import numpy, math

#constants
melody_length = 5150;
l = 50; #notes in scale

#gen random "song"
song = [random.randrange(0,l) for x in xrange(0,melody_length)]

counts = numpy.zeros((l*l,l), dtype=numpy.float)
probs = numpy.zeros((l*l,l), dtype=numpy.float)

combos = []
for i in xrange(0,l):
	for j in xrange(0,l):
		combos.append((i,j))

#for i in xrange(0,len(song)-1):
#	counts[song[i]][song[(i+1)]] += 1 # x is current note, y is next note
 

for i in xrange(2,melody_length):
	for j in xrange(0,l):
		for k in xrange(0,l):
			if (song[i-2] == j and song[i-1] == k):
				counts[j*l+k][song[i-3]] += 1

#add cols for calculating probabilties 

sums = counts.sum(axis=1)

#calc probs from count and sums
for x in xrange(counts.shape[0]):
    for y in xrange(counts.shape[1]):
    	if (not math.isnan(counts[x][y]/sums[x])):
			probs[x][y] = counts[x][y]/sums[x]


#print song

#numpy.set_printoptions(precision=3)

#out = numpy.append(probs,combos,1) #last two columns show input
#print out

print "done"



