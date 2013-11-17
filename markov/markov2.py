import numpy, math, random, pprint

num_notes = 3 # e.g. a,b,c
markov_order = 4 
length_of_song = 10000 

#gen random "song"
song = [random.randrange(0,num_notes) for x in xrange(0,length_of_song)]

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

#generate our markov chain
counts = new_markov(song,markov_order,num_notes) 

#get first N notes
# note, we will need a variation of this function for continuing the chain,
# since for the rest of it, N-1 notes should be used as the input, which will
# reduce our input for the weight foo greatly
out_idx =  weighted_idx(counts.flatten())

print out_idx #linear idx
print idx_convert(out_idx,markov_order,num_notes) #N index





