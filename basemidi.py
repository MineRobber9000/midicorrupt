"""A basic interpretation of MIDI.

We don't need fancy editing, just need to know what is track data and what isn't."""

class MIDILoadError(Exception):
	pass

class MIDIFile:
	def __init__(self,filename):
		# Read data and make data pointer
		with open(filename,"rb") as f:
			self.data = bytearray(f.read())
		self.dp = 0
		try:
			self.loadHeaderChunk()
			assert hasattr(self,"load_format_{!s}".format(self.format)),"Unsupported MIDI format {!s}".format(self.format)
			getattr(self,"load_format_{!s}".format(self.format))()
		except AssertionError as e:
#			raise MIDILoadError("Invalid MIDI: {}".format(e.args[0]))
			pass

	def loadHeaderChunk(self):
		# Check that chunk is indeed a header
		assert self.data[self.dp:self.dp+4]==b"MThd","Invalid header chunk"
		self.dp+=4
		length = self.get32BitValue()
		# Header chunks are always 6 bytes long
		assert length==6,"Header chunk should be 6 bytes long, is {!s}".format(length)
		self.format = self.get16BitValue()
		self.tracks = self.get16BitValue()
		self.division = self.get16BitValue()
		# Format 0 MIDIs have one track only
		assert ((self.tracks==1) if (self.format==0) else True),"Format 0 MIDIs should only have one track"

	def get16BitValue(self):
		a = self.data[self.dp]
		b = self.data[self.dp+1]
		self.dp += 2
		return (a<<8)+b

	def get32BitValue(self):
		a = self.get16BitValue()
		b = self.get16BitValue()
		return (a<<16)+b

	def out16BitValue(self,v):
		a = (v&0xFF00)>>8
		b = (v&0xFF)
		return bytearray((a,b))

	def out32BitValue(self,v):
		a = (v&0xFFFF0000)>>16
		b = (v&0xFFFF)
		ret = self.out16BitValue(a)
		ret.extend(self.out16BitValue(b))
		return ret

	def load_format_0(self):
		assert self.data[self.dp:self.dp+4]==b"MTrk","Invalid track chunk"
		self.dp+=4
		self.track_length = self.get32BitValue()
		self.track = self.data[self.dp:]
		return

	def output_format_0(self,out):
		out.extend(b'MTrk')
		out.extend(self.out32BitValue(self.track_length))
		out.extend(self.track)

	def output(self):
		out = bytearray()
		out.extend(b'MThd')
		out.extend(self.out32BitValue(6))
		out.extend(self.out16BitValue(self.format))
		out.extend(self.out16BitValue(self.tracks))
		out.extend(self.out16BitValue(self.division))
		assert hasattr(self,"output_format_{!s}".format(self.format)),"Unsupported MIDI format {!s}".format(self.format)
		getattr(self,"output_format_{!s}".format(self.format))(out)
		return out
