# midicorrupt

A Python tool for corrupting MIDI files.

## basemidi

A simple, barebones raw MIDI file library. Just validates the MIDI file is formatted correctly and loads. Currently only supports
format 0 MIDIs (single-track). If you want to add support for others, go ahead. See `basemidi.MIDIFile.load_format_0` for a format
loader and `basemidi.MIDIFile.output_format_0` for a format outputter. Both will need to be written for the MIDI file to be
successfully input and output. A correct implementation of the algorithm should produce output of a non-modified MIDIFile object
that is the same as the data from the raw MIDI file.
