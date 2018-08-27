import basemidi

midifile = "canyon.mid" # change this to test another MIDI file

t = basemidi.MIDIFile("canyon.mid")
#print(vars(t))
print("t.format = {!s}".format(t.format))
#print("t.track_length = {!s}".format(t.track_length))
with open("canyon.mid","rb") as f:
	global data
	data = bytearray(f.read())
assert data==t.output(),"Mismatch between file data and output of unmodified object"
print("Correctly implemented output and input routines! Good job!")
