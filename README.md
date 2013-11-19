# Music via algorithm

## How does it work?

Here's a rough sketch of the process:
* Input corpus of midi files
* Extract melodies, chords progressions, rhythms, and song structure
* Generate N-order Markov Chain 
* Create song using probabilities from previous step

## How do I use this?

1. Download files.
2. Run #main.py#.
3. See readme.txt for more details.

## Depedencies
* Uses midicsv for midi conversions
* Uses Python 2.x & the following Python libraries
  * Numpy
  * Math
  * ...

## License
Apache License Version 2.0 - See license.txt for full text.