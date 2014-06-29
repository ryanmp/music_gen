import random, math
from mingus.midi import fluidsynth
from mingus.containers.Instrument import MidiInstrument, Piano
from mingus.containers.Note import Note
import mingus.core.chords as chords
import mingus.core.progressions as progressions
from mingus.containers.Bar import Bar
from mingus.containers.Track import Track
fluidsynth.init("soundfont.sf2")


# returns an array of bars containing a melody
def generate_melody(time_signature, num_bars, key_sig):
	ret = [Bar(key_sig, time_signature) for i in xrange(num_bars)]
	return ret


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
		print l
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

		print chord_lengths


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
			bars[i].place_notes(progression[k],chord_lengths[i])

	return bars


def Gen_Prog(num_chords, num_bars, key_sig):
	raw_progression = generate_progression(num_chords)
	keyed_progression = progressions.to_chords(raw_progression, key_sig)
	return keyed_progression_to_bars(keyed_progression, num_bars, key_sig)


verse = Gen_Prog(4,4,"C#")

t = Track()
for i in verse: t.add_bar(i)

# play it!
fluidsynth.play_Tracks([t], [0], 150)





