import random, math, os, datetime # python modules

# mingus modules
from mingus.midi import fluidsynth
from mingus.containers.Instrument import MidiInstrument
import mingus.core.diatonic as diatonic
from mingus.containers.Note import Note
import mingus.core.chords as chords
import mingus.core.progressions as progressions
from mingus.containers.Bar import Bar
from mingus.containers.Track import Track
from mingus.containers.Composition import Composition


from mingus.containers.Instrument import Instrument, Piano
from mingus.midi import MidiFileOut


sound_fonts = []
for file in os.listdir(os.getcwd()):
    if file.endswith(".sf2"):
        sound_fonts.append(file)

if len(sound_fonts) < 1:
	raise IOError, "current dir must contain at least one soundfont (*.sf2)"
else: fluidsynth.init(sound_fonts[0]) # just use the first one you find by default


'''

info:

	note lengths:
		mathematically speaking, it makes more sense to me to use the following:
			1:whole note, .5:half note, .25:quarter note
		but mingus uses 1, 2, 4... respectively

		So I have decided to use my convention until the moment notes are placed,
		and then they are converted (it's just a basic inversion 1/x) 


todo:

	- after generating a song: i'm currently playing it and saving a midi copy
	  but when i try fluidsythn midi -> wav... it doesn't work
	  is this a problem with a bad header for the midifile, or with fluidsynth?
	  it would be nice to be able to generate midi->wav->mp3 files on the fly for better
	  sharability

	- micro-structure... i.e. partA in structure, broke up into:
	  very simple: (aaaa, abab, abcb, aaab, abba, aabc, abbb, abcc, abbc)...

	- arpegio note of chords? 

	- melody should be able to include 2nd or 3rd voices every now and then

'''

# returns multiple bars containing a melody
def generate_melody(time_sig, num_bars, key_sig, oct_range, num_phrases):
	bars = []
	for i in xrange(num_phrases):
		temp_phrase = generate_phrase(time_sig, num_bars/num_phrases, key_sig, oct_range)
		bars.append(temp_phrase)

	return bars


# returns one long bar containing a melody-piece
def generate_phrase(time_sig, num_bars, key_sig, oct_range):
	empty_bar = Bar(key_sig, (time_sig[0]*num_bars,time_sig[1]))

	possible_notes = diatonic.get_notes(key_sig)
	possible_octaves = [i for i in xrange(oct_range[0],oct_range[1])]
	total_duration = (time_sig[0]/time_sig[1])*num_bars

	possible_note_durations = [.5**i for i in xrange(5)]
	note_durations = []
	while (sum(note_durations) < total_duration):
		next = random.choice(possible_note_durations)
		if sum(note_durations) + next <= total_duration: 
			note_durations.append(next)

	for i in note_durations:
		which_note = random.choice(possible_notes)
		which_octave = random.choice(possible_octaves)
		vel = random.randint(30,127)
		temp_note = Note(which_note, which_octave)
		temp_note.dynamics['velocity'] = vel
		temp_note.velocity = vel

		if random.randint(0,10) > 2:
			empty_bar.place_notes(temp_note,int(1/i))
		else: 
			empty_bar.place_notes(None,int(1/i)) #some number of rests...
	
	return empty_bar


# returns an array containing a unkeyed progression
def generate_progression(num_chords):
	all_major_triads = ["I","II","III","IV","V", "VI","VII"]
	all_major_7ths = [i + "7" for i in all_major_triads]
	all_chords = all_major_triads + all_major_7ths
	ret = []

	for i in xrange(num_chords):
		ret.append(random.choice(all_chords))

	return ret


# this one is a bit complicated... it could use some simplification
def keyed_progression_to_bars(progression, num_bars, key_sig):
	
	# what if num_bars & progression aren't the same?
	# we should pick the appropriate lengths of chords in the progressions...
	# (quarter, half, whole) to fit within the num_bars

	bars = [Bar(key_sig, (4,4)) for i in xrange(num_bars)]
	prog_length = len(progression)
	chord_lengths = []

	# if more chord than bars, tries to divide up chords as to fit 
	if prog_length >= num_bars:
		l = float(num_bars)/prog_length

		this_value = l
		round_to = [1] + [.5**i for i in xrange(6)]
		rounded = this_value
		for i in round_to:
			if this_value < i:
				rounded = i
			else:
				rounded = i
				break
		l = rounded

		chord_lengths = [l for i in xrange(prog_length)]

		# completely random is still a problem... for instance 1, 2, 1, 2 would break
		# because the second one wouldn't fit in the measure... this needs to be broken up into measures
		# or even better, just disregard the convention for bars... and have each progression be one long
		# bar for simplicity
		while( sum(chord_lengths) < num_bars):
			idx = random.randint(0,len(chord_lengths))
			chord_lengths[idx] = .5/chord_lengths[idx]
		
	else: 
		print "do something else"

	# .5 -> 2, .25 -> 4

	chord_lengths = [int(1/x) for x in chord_lengths]

	k = -1
	for i in xrange(len(bars)):
		for j in xrange(chord_lengths[i]):
			k += 1

			vel = random.randint(55,110)
			this_chord = []
			for note in progression[k]:
				temp_note = Note(note,3)
				this_vel = vel + random.randint(-15,15)
				temp_note.dynamics['velocity'] = this_vel
				temp_note.velocity = this_vel
				this_chord.append(temp_note)  #octave = 4, dyn=.5 ... still not working!


			bars[i].place_notes(this_chord,chord_lengths[i])

	return bars


def Gen_Prog(num_chords, num_bars, key_sig):
	raw_progression = generate_progression(num_chords)
	keyed_progression = progressions.to_chords(raw_progression, key_sig)
	return keyed_progression_to_bars(keyed_progression, num_bars, key_sig)


def Gen_Section(key, num_bars):
	melody = generate_melody((4,4),num_bars,key,(4,6),2) 
	chords = Gen_Prog(4,num_bars,key)
	return melody, chords


# generates large scale song structure (e.g. verse, chorus1, verse2, chorus)
# returns a choice as an array -> interpretted by Gen_Song
def Gen_Song_Structure():
	l = []
	l.append ([0,1,0,1,0])
	l.append ([0,1,2,1,0])
	l.append ([0,1,0,1,2,1])
	l.append ([0,1,0,2,0])
	l.append ([0,1,0,1,2])
	l.append ([0,1,2,0,1])
	l.append ([0,1,2,0,2])
	l.append ([0,1,2,0,1,2])
	l.append ([0,1,2,0,1,2,1])
	return random.choice(l)


def Gen_Song(key):
	structure = Gen_Song_Structure()

	print 'structure', structure

	parts = []
	for i in xrange(len(set(structure))):
		part = Gen_Section(key,2) # should randomize number of bars too...
		parts.append(part)

	song = []
	for i in structure:
		song.append( parts[i] )

	return song


def Play_Song(song):
	c = Composition()

	instrument = MidiInstrument()
	instrument.instrument_nr = 0
	t1 = Track(instrument)
	t2 = Track(instrument)

	for part in song:
		for i in part[0]:
			t1.add_bar(i)
		for i in part[1]:
			t2.add_bar(i)
	c.add_track(t1)
	c.add_track(t2)

	#fluidsynth.set_instrument(0, 0)
	#fluidsynth.set_instrument(1, 0)

	fluidsynth.play_Tracks(c.tracks, [0 for i in xrange(len(c.tracks))])


def Save_Song(song,dt):
	c = Composition()

	instrument = MidiInstrument()
	instrument.instrument_nr = 0
	t1 = Track(instrument)
	t2 = Track(instrument)

	for part in song:
		for i in part[0]:
			t1.add_bar(i)
		for i in part[1]:
			t2.add_bar(i)
	c.add_track(t1)
	c.add_track(t2)

	file_dir = "midi_archive/"
	midi_file_name = file_dir + 'song_' + dt.strftime("%Y%m%dT%H%M%SMS%f") + '.midi'
	MidiFileOut.write_Composition(midi_file_name,c)

	# also saving as an mp3 (using a os lib called timidity)?
	file_dir = "/mp3_archive/"
	mp3_file_name = file_dir + 'song_' + dt.strftime("%Y%m%dT%H%M%SMS%f") + '.mp3'
	os.system('timidity -Ow -o - ./' + midi_file_name + ' | lame - ./' + mp3_file_name)


	

'''

What follows is a sample of what we can do with these functions....


'''



song_key_sig = random.choice(diatonic.basic_keys)
song = Gen_Song(song_key_sig)

time_stamp = datetime.datetime.now()

Save_Song(song,time_stamp)
Play_Song(song)










