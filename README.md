# midi_to_tidalcycles
Command-line tool for converting polyphonic midi files to tidalcycles syntax.

## Requirements
* Numpy (tested on version 1.12.1)

* Python midi module (requires Python 2.  tested on version 2.7.13)
https://github.com/vishnubob/python-midi

## Description
Use this tool to take a midi file generated by a digital audio workstation (DAW) and convert it to a TidalCycles expression.

`python midi_to_tidalcycles.py [OPTIONS] [MIDIFILE...]`

Polyphonic midi phrases will be converted to a TidalCycles stack.  `# amp` patterns (similar to midi velocity which is between 1 and 127 but ranging between 0.0 and 1.0 in TidalCycles syntax) and `# legato` patterns.

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
to standard out.  This "stack" expression can be copied and pasted into TidalCycles.  Append ` # s "midi" # midichan 0` to this stack to start sending your midi signal from TidalCycles.

## Options

```
-e, --events            print midi event information
-d, --debug             print midi event information, voice numbers, and quanta numbers for debugging
-s, --shape             print midi shape (number of quanta and polyphonic voices)
-q, --resolution        specify number of quanta per quarter note
-l, --legato            print legato pattern
-a, --amp               print amplitude pattern
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

### Multiple midi files at once

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

