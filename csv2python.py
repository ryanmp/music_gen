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

song_as_list = csv2list('test.csv')