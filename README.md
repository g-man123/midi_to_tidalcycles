# midi_to_tidalcycles
Command-line tool for converting polyphonic midi files to tidalcycles syntax.

## Requirements
* Numpy (tested on version 1.12.1)

* Python midi module (requires Python 2.  tested on version 2.7.13)
https://github.com/vishnubob/python-midi

## Description
Use this tool to take a midi file generated by a digital audio workstation (DAW)

`python midi_to_tidalcycles.py [OPTIONS] [MIDIFILE...]`

## Example usage

`python midi_to_tidalcycles.py -al ../test_examples/insen_quarter-eighth-notes_duophonic_125bpm.mid`

prints

```../test_examples/insen_quarter-eighth-notes_duophonic_125bpm.mid
inferred polyphony is 2```

```haskell
stack [
    n "f5 ~ ~ ~ cs5 ~ ~ ~ c5 ~ ~ ~ gs4 ~ c5 ~ cs5 ~ c5 ~ gs4 ~ g4 ~ ~ ~ ~ ~ ~ ~ ~ ~"
    # amp "0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0"
    # legato "4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0",
    n "c6 ~ ~ ~ gs5 ~ ~ ~ g5 ~ ~ ~ f5 ~ g5 ~ gs5 ~ g5 ~ f5 ~ ds5 ~ ~ ~ ~ ~ ~ ~ ~ ~"
    # amp "0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.0 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.79 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0"
    # legato "4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0"
]```
to standard out.  This "stack" expression can be copied and pasted into TidalCycles.  Append ` # s "midi" # midichan 0` to this stack to start sending midi signals from TidalCycles!

## Options

`
-e, --events            print midi event information
-d, --debug             print midi event information, voice numbers, and quanta numbers for debugging
-s, --shape             print midi shape (number of quanta and polyphonic voices)
-q, --resolution        specify number of quanta per quarter note
-l, --legato            print legato pattern
-a, --amp               print amplitude pattern
`


