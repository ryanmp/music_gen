import numpy, math, random, pprint

'''
At this point I really need to SPEED UP the montecarlo function,
here's how I'm going to tackle it:

Convert N-dim array from markov chain into tuple-list with N-indices as key,
and COUNT as value. Remove zeroes from dict. create new tuple-list where
count gets distributed to multiple entries. each entry has N-indices.

Then we can randomly choose from this list, and we will have the appropriately
weighted probabilities represented.

Yeah, I'm currently iterating over way too many zero values. 

It is possible that once corpus gets MUCH MUCH bigger, this new method won't
help much anymore, but it's still worth working on for now.
'''

num_notes = 56 # e.g. a,b,c
markov_order = 2 
length_of_song = 1146 

#pass in 'FILE.CSV' formatted via midicsv (midi to csv)
#returns a list
def csv2list(_csvmidifile):
	data = open(_csvmidifile).read()
	dl = [line.split(',') for line in data.split('\n')]
	dl2 = []
	for i in xrange(0,len(dl)-1):
		if ((dl[i][2] == ' Note_on_c') and (dl[i][5] != ' 0')):
			dl2.append(int(dl[i][4]))
	return dl2

def new_markov(_song, _order, _num_notes):
	#instantiate ND array
	counts = numpy.zeros([_num_notes] * _order, dtype=numpy.float) 

	#work linearly through song
	for i in xrange(len(_song)-(_order-1)):

		idx = []
		for j in xrange(0,_order): # for (i,i+1,i+n...) ~ idx
			idx.append(_song[i+j])

		idx = tuple(idx)

		counts.itemset(idx,counts.item(idx)+1)

	return counts

#so I don't actually need this anymore, my weighted prob function takes care of it for me
def counts_to_probs(_arr):
	tmp_sum = numpy.sum(_arr)
	_arr = _arr/tmp_sum
	return _arr

#given a 1d list of counts or probs, it'll return a the idx of one of the values, using the 
#appropriate weighting to the randomness
def weighted_idx(_weights):
	choice = random.random() * sum(_weights)
	for i, w in enumerate(_weights):
	    choice -= w
	    if choice < 0:
	        return i

#given the linear index from weighted_idx, it returns a list of the N indices
def idx_convert(input, _order, _num_notes):
	t = [-1] * _order
	m = _num_notes
	for i in xrange(0,_order):
		t[i] = input/(m**(_order-1-i))%num_notes
	return t


#gen random "song"
#song = [random.randrange(0,num_notes) for x in xrange(0,length_of_song)]
#counts = new_markov(song,markov_order,num_notes) 
#print(counts)

print ('generating markov...')
song2 = csv2list('test.csv')
num_notes2 = max(song2)+1
counts2 = new_markov(song2,4,num_notes2) 
#print(counts2)



#get first N notes
# note, we will need a variation of this function for continuing the chain,
# since for the rest of it, N-1 notes should be used as the input, which will
# reduce our input for the weight foo greatly

print ('montecarlo simulation...')
out_idx =  weighted_idx(counts2.flatten())
out_idx2 = idx_convert(out_idx,4,num_notes2)
print(out_idx2)
