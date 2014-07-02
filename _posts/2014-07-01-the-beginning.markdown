---
layout: post
title:  "The Beginning"
date:   2014-07-01 08:48:08
categories: 
---

> As machines become more and more efficient and perfect, so it will become clear that imperfection is the greatness of man. ~ Ernst Fischer

Beginning with a very broad question:

How can we use data & algorithms to help us compose music?

Music, if it is recognizable and it appeals to our sensibilities, does so in part because it adheres to a set of conventions. This doesn't define what music IS, but it gives us a good foundation on which to begin. If we encode these rules, and then follow them to some degree, what is created should sound roughly 'musical'. And this is where my work begins.

I'm not starting from scratch - I'm sure I will encorporate a number of different tools/libraries/frameworks in order to make life easier.

The first thing I came across is called [Mingus](https://code.google.com/p/mingus/). This allows me to use the vocabulary of music theory (notes, bars, keys, chords, etc.) without having to define the relationship between all these concepts since the library has already done this. 

For example:

{% highlight python %}
n = Note('C',3,100) # 'note', 'octave', 'velocity/volume'
b = Bar()
b.place_note(n)
t = Track()
t.add_bar(b)
c = Composition()
c.add_track(t)
{% endhighlight %}

And now I have a 'composition' which can be saved/played as a midi file.

## What am I building using Python+Mingus?

My first goal is to write a serious of generators. These will eventually be able to accept a whole slew of parameters which will determine all sorts of qualities, but in the beginning they will be simple and random.

This is going to be a bit of an information dump, so feel free to jump to the end of this post to hear an example of the current state of this program, and then move on to the next posts. I promise these will be more interesting and singular, as I am able to focus on whatever particular aspect I am trying to improve - rather than just trying to get you caught up with all my preliminary work. 

### Song Generator

Here is the entry point. It currently just sets the rest of the generators in motion. It first calls the structure generator.

### Macro-Structure Generator

This chooses from a set of possible song structures. You may be familiar with the default structure of a pop-song: verse 1, chorus, verse 2, chorus, bridge, chorus.

In the structure generator this would be described as something like: [a1,b,a2,b,c,b] -> just a list of parts where the number of symbols describes the unique set of parts.

### Micro-Structure Generator

Something like a verse isn't typically just a single chord progression and a melody (it can be, but we would like to include some other possibilities, too). So this picks a structure for each part, much in the same way as the previous structure generator.

### Part Generator

Okay, now we can get a bit more specific. It would be nice to allow this to be more general, but I'm starting simple. So the part generator calls the chord progression and melody generators, and then simply overlays the two so that they happen simultaneously.

### Chord Progression Generator

This starts by assuming that we want chords that fall within a single key. It chooses a number of chords first in the general form (e.g. I, II, IV), and then renders these chords into the specified key by picking the notes making up these chords (within a particular octave). So far, nothing really has been chosen as to how these chords are played - no patterns or rhythms have been included. The velocity of each chord is chosen at random, and the notes within the chord are given a little bit of velocity variation.

### Melody Progression Generator

So ideally this would work in conjunction with the chord progression generator - we want there to be a relationship between which notes are chosen to be played on top of which chords. But of course, in its initial state, this is also basic and random. It just picks a series of notes in our key, and picks random velocities, and semi-random durations (such that it still fits properly in the number of bars specified.)

And that's it! After the song generator runs all of the other generators, the program spits out a file containing hundreds of notes, all of them in some particular key, with some basic relationships and patterns built in.

## The State of Things Thus Far

So here are a few examples of what this currently sounds like (listed by the seed given to the random number generator):

+ [1234](1234.mp3)
+ [5656](1234.mp3)

Thanks for reading! Check back again later if you want to read about (or listen to) my progress. 
 





