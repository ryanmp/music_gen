'''
todo:

perhaps during csv to python list conversion...
I was going to use the key information to shift to a standard key
this way the amount of info I import is ~ 12x more useful. The key we play 
a piece in isn't as important as the relative relationship between notes..
i.e.,all songs will be converted to the key of C for the reason. 

'''

import os
import markov

def main(p):
	midi_files_ls = get_midi_files(p)
	midi_to_csv(midi_files_ls,p)
	csv_files_ls = get_csv_files(p)
	python_list = csv_2_list(p,csv_files_ls)

	counts = markov.new_markov(python_list[0],2,max(python_list[0])+1)


#gets all '.mid' files stored in '/input'	
def get_midi_files(p):
	in_path = p+"/input/"
	all_files = os.listdir(in_path)
	midi_files = []
	for fs in all_files:
		if fs.endswith(".mid"):
			midi_files.append(fs)
	return midi_files

#uses midicsv for conversion
#output located in '/temp/'
def midi_to_csv(in_files,p):
	print "converting all midi files to csv"
	process_this_vid_cmd = "midicsv/midicsv "
	for fs in in_files:
		os.system(process_this_vid_cmd+p+"/input/"+fs+" "+p+"/temp/"+fs+".csv")

#gets all '.csv' files stored in '/temp'	
def get_csv_files(p):
	in_path = p+"/temp/"
	all_files = os.listdir(in_path)
	csv_files = []
	for fs in all_files:
		if fs.endswith(".csv"):
			csv_files.append(fs)
	return csv_files

#pass in 'file.csv'
#returns a list
def csv_2_list(p,_files):

	all_songs = []

	for fs in _files:
		data = open(p+"/temp/"+fs).read()
		dl = [line.split(',') for line in data.split('\n')]
		dl2 = []
		for i in xrange(0,len(dl)-1):
			if ((dl[i][2] == ' Note_on_c') and (dl[i][5] != ' 0')):
				dl2.append(int(dl[i][4]))
		all_songs.append(dl2)
	return all_songs

# assuming you are in the same dir
# as main
main(os.getcwd())


if __name__ == "__main__":
    x= main()
    print( x )