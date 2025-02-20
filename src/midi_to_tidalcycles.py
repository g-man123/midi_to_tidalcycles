from __future__ import print_function
import midi
import numpy as np
import os
import argparse


def midinote_to_note_name(midi_note):
    if midi_note == 0.0:
        return "~"
    elif midi_note == 99999:
        return 0
    midi_note = int(midi_note) # 1 - 127
    # note_names_array = ["c", "cs", "d", "ds", "e", "f", "fs", "g", "gs", "a", "as", "b"]
    # q, r = divmod(midi_note, 12) 
    # note_name = note_names_array[r]
    # octave_name = q  # q - 1  <- this is correct but tidal is off by an octave I think.
    # full_note_name = str(note_name) + str(octave_name)
    # return full_note_name
    return midi_note


def infer_polyphony(midi_pattern):
    last_event = midi_pattern[-1][-1]
    assert type(last_event) == midi.events.EndOfTrackEvent
    n_adjacent_on_events = 0
    inferred_polyphony = 0
    for index, event in enumerate(midi_pattern[-1]):
        if type(event) == midi.events.NoteOnEvent: # starting note on 
            n_adjacent_on_events += 1
            inferred_polyphony = max(inferred_polyphony, n_adjacent_on_events)
        elif type(event) == midi.events.NoteOffEvent:
            n_adjacent_on_events = 0
    return inferred_polyphony

def find_notes(midi_pattern):
    notes = [x.pitch for x in midi_pattern if type(x) == midi.events.NoteOnEvent or type(x) == midi.events.NoteOffEvent]
    notes = sorted(list(dict.fromkeys(notes)))
    return(len(notes), notes)

def midi_to_array2(filename, quanta_per_qn = 4, velocity_on = False, legato_on = False, print_events = False, debug = False, hide = False, polyphonic_mode = False, show_pitch = False):
    pattern = midi.read_midifile(filename)
    ticks_per_quanta = pattern.resolution/quanta_per_qn  # = ticks per quarter note * quarter note per quanta
    last_event = pattern[-1][-1]
    assert type(last_event) == midi.events.EndOfTrackEvent
    cum_ticks = 0
    for index, event in enumerate(pattern[-1]):
        cum_ticks += event.tick
    # this int() is just for type matching in python 3 and shouldn't be rounding anything-- 
    # n_quanta should already be an int.
    n_quanta = int(cum_ticks/ticks_per_quanta)
    n_notes, notes_list = find_notes(pattern[-1])
    polyphony = infer_polyphony(pattern)
    if polyphonic_mode:
        n_lines = polyphony
    else:
        n_lines = n_notes
    if not hide and polyphony and polyphonic_mode:
        print("inferred polyphony is ", end = "")
        print(polyphony)
    note_vector = np.zeros((n_quanta, n_lines))
    if velocity_on:
        velocity_vector = np.zeros((n_quanta, n_lines))
    if legato_on:
        legato_vector = np.zeros((n_quanta, n_lines))
        currently_active_notes = {} 
    cum_ticks = 0
    voice = -1 
    
    for event in pattern[-1]:
        if print_events or debug:
            print(event)
        cum_ticks += event.tick
        if type(event) == midi.events.NoteOnEvent:
            voice += 1
            quanta_index = int(cum_ticks/ticks_per_quanta)
            note_index = notes_list.index(event.pitch)
            if debug:
                print("voice number ", end = "")
                print(voice)
                print("quanta number ", end = "")
                print(quanta_index)
            if polyphonic_mode:
                note_vector[quanta_index,voice] = event.pitch
            elif show_pitch:
                note_vector[quanta_index,note_index] = event.pitch
            else:
                if note_index == 0:
                    note_vector[quanta_index,note_index] = 99999
                else:
                    note_vector[quanta_index,note_index] = note_index
            if legato_on:
                if polyphonic_mode:
                    currently_active_notes[event.pitch] = [quanta_index, voice]
                else:
                    currently_active_notes[event.pitch] = [quanta_index, note_index]
            if velocity_on:
                if polyphonic_mode:
                    velocity_vector[quanta_index,voice] = event.velocity
                else:
                    velocity_vector[quanta_index,note_index] = event.velocity
        elif (type(event) == midi.events.NoteOffEvent) & (legato_on):
            quanta_note_off_index = int(cum_ticks/ticks_per_quanta)
            note_length = quanta_note_off_index - currently_active_notes[event.pitch][0]
            legato_vector[currently_active_notes[event.pitch][0],currently_active_notes[event.pitch][1]] = note_length
            del currently_active_notes[event.pitch]
            voice = -1 #-= 1 
        else: # end of track
            # turn all notes off
            quanta_note_off_index = int(cum_ticks/ticks_per_quanta)
            try:
                note_index = notes_list.index(event.pitch)
            except:
                pass
            if legato_on:
                for key in currently_active_notes.keys():
                    note_length = quanta_note_off_index - currently_active_notes[key][0]
                    if polyphonic_mode:
                        legato_vector[currently_active_notes[key],voice] = note_length
                    else:
                        legato_vector[currently_active_notes[key],note_index] = note_length
            voice = -1
    if not legato_on and velocity_on:
        return note_vector, velocity_vector

    elif not velocity_on and legato_on:
        return note_vector, legato_vector

    elif velocity_on and legato_on:
        return note_vector, velocity_vector, legato_vector

    else:
        return note_vector





def vel_to_amp(vel):
    return round(vel/127., 2)

def simplify_repeats(list_pattern):
    """
    Converts ['a','a','b','a','b', 'b','b'] to ['a!2', 'b','a','b!3']
    """
    n_repeats = 0
    output_list = []
    for i, x in enumerate(list_pattern):
        # if not the last element
        if i != len(list_pattern) - 1:
            # if the next element is a repeat
            # increment the counter
            if x == list_pattern[i + 1]:
                n_repeats += 1
            # if next element is different and current element is not a repeat.
            elif n_repeats == 0:
                output_list.append(x)
            # otherwise there was a repeat that terminates now.
            else: 
                new_x = str(x) + '!' + str(n_repeats + 1)
                output_list.append(new_x) 
                n_repeats = 0
        # handle last element
        else:
            # simple case, last element is not a repeat
            if n_repeats == 0:
                output_list.append(x)
            # the penultimate position matches the last. 
            else:
                new_x = str(x) + '!' + str(n_repeats + 1)
                output_list.append(new_x) 
                n_repeats = 0

    return output_list


def print_midi_stack(notes, vels = None, legatos = None, consolidate = None, tab = None):
    n_lines = len(notes[0,:])
    # determine whether a stack is needed and create a control boolean
    add_stack = (n_lines != 1) | (vels is not None) | (legatos is not None)
    if add_stack:
        print("stack [")
    # iterate over lines
    for j in range(0,n_lines):
        notes_names  = [midinote_to_note_name(x) for x in notes[:,j]]
        if consolidate:
            notes_names = simplify_repeats(notes_names)
        if tab:
            print("    n \"", end = "")
        else:
            print("\"", end = "")
        print(*notes_names, sep=' ', end = "")
        if (legatos is None) & (vels is None) & (j != n_lines - 1): # add a quote and a comma if there are more voices in the stack
            print("\",")  
        else:
            print("\"") # else this is the last voice, so close the quotes
        if vels is not None:
            print("    # amp \"", end = "")
            note_vels  = [vel_to_amp(x) for x in vels[:,j]]
            if consolidate:
                note_vels = simplify_repeats(note_vels)
            print(*note_vels, sep=' ', end = "")
            # add comma if it's not the last voice and if there are no legatos
            if legatos is None:
                if not j == len(notes[0,:]) - 1:
                    print("\",")
                # otherwise close the stack
                else:
                    print("\"\n]")
            else:  # if legatos is not None 
                print("\"")
        if legatos is not None:
            print("    # legato \"", end = "")
            note_legatos  = [x for x in legatos[:,j]]
            # note_legatos  = [midinote_to_note_name(x) for x in legatos[:,j]]
            if consolidate:
                note_legatos = simplify_repeats(note_legatos)
            print(*note_legatos, sep=' ', end = "")
            # add comma if it's not the last voice
            if not j == len(notes[0,:]) - 1:
                print("\",")
            # otherwise close the stack
            else:
                print("\"\n]")
        if (legatos is None) & (vels is None) & (j == n_lines - 1) & (add_stack):
            print("]")





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("midi_files",nargs="*")
    parser.add_argument("--events","-e", const = True, default = False, help = "print midi event information", action = 'store_const')
    parser.add_argument("--debug","-d", const = True, default = False, help = "print midi event information, voice numbers, and quanta numbers for debugging", action = 'store_const')
    parser.add_argument("--shape","-s", const = True, default = False, help ="print midi shape", action = 'store_const')
    parser.add_argument("--resolution","-q", default = 4, type = int, help = "specify number of quanta per quarter note")
    parser.add_argument("--legato","-l", const = True, default = False, help = "print legato pattern", action = 'store_const')
    parser.add_argument("--amp","-a", const = True, default = False, help = "print amplitude pattern", action = 'store_const')
    parser.add_argument("--consolidate","-c", const = True, default = False, help = "consolidate repeated notes and values with '!' notation", action = 'store_const')
    parser.add_argument("--hide","-H", const = True, default = False, help = "hide printing name of midi file and inferred polyphony", action = 'store_const')
    parser.add_argument("--tab","-t", const = True, default = False, help = "add tabs to start of each line", action = 'store_const')
    parser.add_argument("--polyphony","-p", const = True, default = False, help = "polyphonic style of transcript", action = 'store_const')
    parser.add_argument("--pitch","-pi", const = True, default = False, help = "show pitch in transcript", action = 'store_const')
    args = parser.parse_args()
    for midi_file in args.midi_files:
         if not args.hide:
             print(midi_file)
         data = midi_to_array2(midi_file, quanta_per_qn = args.resolution, velocity_on = args.amp, legato_on = args.legato, print_events = args.events, debug = args.debug, hide = args.hide, polyphonic_mode = args.polyphony, show_pitch = args.pitch)
         vels = None
         legatos = None
         consolidate = None
         if args.amp:
             if args.legato:
                 notes, vels, legatos = data
             else:
                 notes, vels = data
         elif args.legato:
                 notes, legatos = data
         else:
             notes = data
         if args.shape:
             print('quanta: ',end = '')
             print(notes.shape[0])
             print('voices: ',end = '')
             print(notes.shape[1])
         # syncs tempo across all midis!
         slow_cmd = "slow (" + str(notes.shape[0]/args.resolution) + "/4) $ "
         print(slow_cmd, end = "")
         print_midi_stack(notes, vels, legatos, consolidate = args.consolidate, tab = args.tab)
