# midi_to_tidalcycles
Command-line tool for converting polyphonic MIDI files to TidalCycles syntax.  


(Extreme) example of a >4 minute piano improvisation converted to TidalCycles code with pitch, note velocity, and legato data preserved:
![Alt text](figures/tc_from_midi_piano.png?raw=true "Extreme Code Example")

Example of MIDI data produced by the above TidalCycles code (zoomed in to show velocities and note length):
![Alt text](figures/reconstructed_midi.png?raw=true "Example of a reconstructed MIDI file")

## Requirements
* Numpy (Tested on numpy version 1.12.1)

* [Python midi module](https://github.com/vishnubob/python-midi) (Requires Python 2.  Tested on Python 2.7.13.  Sorry, I wish their midi module worked in Python 3! With conda however it is easy swiitching between python versions--[this article](https://docs.anaconda.com/anaconda/user-guide/tasks/switch-environment/) walks you through how to do that.) 

## Description
Use this tool to take a MIDI file generated by a DAW or instrument and convert it to a TidalCycles expression.

`python midi_to_tidalcycles.py [OPTIONS] [MIDIFILE...]`

Polyphonic MIDI phrases will be converted to a TidalCycles stack.  Optional arguments allow for adding `# amp` patterns (similar to midi velocity which is between 1 and 127 but ranging between 0.0 and 1.0 in TidalCycles syntax), adding `# legato` patterns, simplifying the generated expression, and controlling rhythmic quantization.  Multiple separate MIDI files can be translated to TidalCycles in one command.

For an intro to sending MIDI signals from TidalCycles to your synthesizers and drum machines, check out [Kindohm's youtube tutorial](https://www.youtube.com/watch?v=_yKWWSc6zY8).

## Example usage

`python midi_to_tidalcycles.py -al ../test_examples/insen_quarter-eighth-notes_duophonic_125bpm.mid`

prints

```
../test_examples/insen_quarter-eighth-notes_duophonic_125bpm.mid
inferred polyphony is 2
```

```haskell
stack [
    n "f5 ~ ~ ~ cs5 ~ ~ ~ c5 ~ ~ ~ gs4 ~ c5 ~ cs5 ~ c5 ~ gs4 ~ g4 ~ ~ ~ ~ ~ ~ ~ ~ ~"
    # amp "0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0"
    # legato "4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0",
    n "c6 ~ ~ ~ gs5 ~ ~ ~ g5 ~ ~ ~ f5 ~ g5 ~ gs5 ~ g5 ~ f5 ~ ds5 ~ ~ ~ ~ ~ ~ ~ ~ ~"
    # amp "0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0"
    # legato "4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0"
]
```
to standard out.  This "stack" expression is intended to be copied and pasted into TidalCycles.  Prepend something like `d1 $ slow 8 $` and append ` # s "midi" # midichan 0` to this stack to start sending your MIDI signal from TidalCycles.

## Options

```
-q, --resolution        specify number of quanta per quarter note
-l, --legato            print legato pattern
-a, --amp               print amplitude pattern
-c, --consolidate       simplify repeating values using mini-notation 
-e, --events            print MIDI event information
-d, --debug             print MIDI event information, voice numbers, and quanta numbers for debugging
-s, --shape             print MIDI shape (number of quanta and polyphonic voices)
-H, --hide              hide inferred polyphony and midi file info (useful for automatic copying of tidalcycles code) 
```

## More examples

### Basic use

`python midi_to_tidalcycles.py  ../test_examples/simple_legato_monophonic.mid`

```../test_examples/simple_legato_monophonic.mid
inferred polyphony is 1
```

```haskell
    n "c5 d5 ds5 ~ f5 d5"
```



### Adding amplitude (MIDI note velocity) to a duophonic file

`python midi_to_tidalcycles.py -a  ../test_examples/simple_legato_duophonic.mid`


```
../test_examples/simple_legato_duophonic.mid
inferred polyphony is 2
```

```haskell
stack [
    n "c5 d5 ds6 ds5 f5 d5"
    # amp "0.79 0.79 0.39 0.79 0.79 0.79",
    n "c6 d6 ~ ~ f6 d6"
    # amp "0.39 0.39 0.0 0.0 0.39 0.39"
]
```


### Adding amplitude, legato, and changing the resolution (notes per quarternote, or *degree of quantization*)

`python midi_to_tidalcycles.py  -al -q 16 ../test_examples/simple_legato_duophonic.mid`

```
../test_examples/simple_legato_duophonic.mid
inferred polyphony is 2
```

```haskell
stack [
    n "c5 ~ ~ ~ d5 ~ ~ ~ ds6 ~ ~ ~ ds5 ~ ~ ~ f5 ~ ~ ~ d5 ~ ~ ~"
    # amp "0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.39 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0"
    # legato "4.0 0.0 0.0 0.0 8.0 0.0 0.0 0.0 8.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0",
    n "c6 ~ ~ ~ d6 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ f6 ~ ~ ~ d6 ~ ~ ~"
    # amp "0.39 0.0 0.0 0.0 0.39 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.39 0.0 0.0 0.0 0.39 0.0 0.0 0.0"
    # legato "4.0 4.0 0.0 0.0 4.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0"
]
```

### Simplifying the generated TidalCycles code by consolidating repeating neighboring values (recommmended). 

The '-c' or '--consolidate' flag simplifies the resulting TidalCycles expression by combining adjacent repeating values using the '!' mini-notation.
The following shows how the above example is simplified with consolidation.   


`python midi_to_tidalcycles.py  -alc -q 16 ../test_examples/simple_legato_duophonic.mid`                       


```
../test_examples/simple_legato_duophonic.mid
inferred polyphony is 2
```

```haskell
stack [
    n "c5 ~!3 d5 ~!3 ds6 ~!3 ds5 ~!3 f5 ~!3 d5 ~!3"
    # amp "0.79 0.0!3 0.79 0.0!3 0.39 0.0!3 0.79 0.0!3 0.79 0.0!3 0.79 0.0!3"
    # legato "4.0 0.0!3 8.0 0.0!3 8.0 0.0!3 4.0 0.0!3 4.0 0.0!7",
    n "c6 ~!3 d6 ~!11 f6 ~!3 d6 ~!3"
    # amp "0.39 0.0!3 0.39 0.0!11 0.39 0.0!3 0.39 0.0!3"
    # legato "4.0!2 0.0!2 4.0 0.0!11 4.0 0.0!3 4.0 0.0!3"
]
```


You can see how the neighboring rests are grouped together now.  More complex examples can be much worse without consolidation!

### Multiple MIDI files at once

`python midi_to_tidalcycles.py -al ../test_examples/jazz-chords_played-live_quadraphonic_125bpm.mid ../test_examples/simple_legato_monophonic.mid`

```../test_examples/jazz-chords_played-live_quadraphonic_125bpm.mid
inferred polyphony is 4
```

```haskell
stack [
    n "e4 ~ ~ ~ gs4 ~ ~ ~ a4 ~ ~ ~ gs4 ~ ~ ~ g4 ~ ~ ~ gs4 ~ ~ ~ a4 ~ ~ ~ b4 ~ ~ ~"
    # amp "0.47 0.0 0.0 0.0 0.43 0.0 0.0 0.0 0.47 0.0 0.0 0.0 0.42 0.0 0.0 0.0 0.12 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.2 0.0 0.0 0.0 0.51 0.0 0.0 0.0"
    # legato "2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0",
    n "c4 ~ ~ ~ f4 ~ ~ ~ e4 ~ ~ ~ b4 ~ ~ ~ a4 ~ ~ ~ d5 ~ ~ ~ g5 ~ ~ ~ c5 ~ ~ ~"
    # amp "0.43 0.0 0.0 0.0 0.39 0.0 0.0 0.0 0.49 0.0 0.0 0.0 0.46 0.0 0.0 0.0 0.46 0.0 0.0 0.0 0.54 0.0 0.0 0.0 0.46 0.0 0.0 0.0 0.57 0.0 0.0 0.0"
    # legato "2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0",
    n "g4 ~ ~ ~ d4 ~ ~ ~ g4 ~ ~ ~ d5 ~ ~ ~ e5 ~ ~ ~ f5 ~ ~ ~ c5 ~ ~ ~ e5 ~ ~ ~"
    # amp "0.5 0.0 0.0 0.0 0.46 0.0 0.0 0.0 0.48 0.0 0.0 0.0 0.48 0.0 0.0 0.0 0.31 0.0 0.0 0.0 0.55 0.0 0.0 0.0 0.37 0.0 0.0 0.0 0.61 0.0 0.0 0.0"
    # legato "2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0",
    n "a4 ~ ~ ~ b4 ~ ~ ~ c5 ~ ~ ~ f4 ~ ~ ~ c5 ~ ~ ~ b4 ~ ~ ~ e5 ~ ~ ~ ~ g5 ~ ~"
    # amp "0.47 0.0 0.0 0.0 0.39 0.0 0.0 0.0 0.43 0.0 0.0 0.0 0.48 0.0 0.0 0.0 0.47 0.0 0.0 0.0 0.52 0.0 0.0 0.0 0.49 0.0 0.0 0.0 0.0 0.42 0.0 0.0"
    # legato "2.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 0.0 2.0 0.0 0.0"
]
```

```
../test_examples/simple_legato_monophonic.mid
inferred polyphony is 1
```

```haskell
stack [
    n "c5 d5 ds5 ~ f5 d5"
    # amp "0.79 0.79 0.79 0.0 0.79 0.79"
    # legato "1.0 1.0 2.0 0.0 1.0 1.0"
]
```

