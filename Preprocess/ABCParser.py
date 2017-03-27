# ABC Parser for ABC Music Notation Files

from __future__ import division

import re
import string
import math
from Preprocess import GlobalConstant


class TuneBook(object):
	"""
	Represents a tunebook with tunes and free text.

	Properties
	----------
	text
		An array of free text blocks, as strings.
	tune
		An array of tunes, as Tune objects.
	"""

	def __init__(self, filename=None):
		"""
		Creates a TuneBook object. If a filename is given, the file is opened
		and parsed. If an invalid filename is given, throws IOError.
		"""

		self.text = []    	# array of text blocks as strings
		self.tune = []   	# array of tunes as Tune

		if filename:
			f = open(filename, 'Ur')
			self.parse(f.read())
			f.close()

	def parse(self, str):
		"""
		Parses the given input.
		"""
		for lines in str.split('\n\n'):
			if 'x:' in lines.lower():
				tune = Tune()
				tune.parse(lines)
				self.tune.append(tune)
			else:
				self.text.append(lines)


##############################################################################
class Tune(object):
	"""
	Represents an entire tune with information fields and music.

	Properties
	----------
	text
		An array of the lines of the tune, as strings.
	line
		An array of the lines of the tune, as Line objects (see below).
	"""

	def __init__(self, filename=None):
		"""
		Creates a Tune object. If a filename is given, the file is opened and
		parsed.If an invalid filename is given, throws IOError.
		"""

		self._fields = {}	# information fields
		self.text = []    	# array of tune lines as strings
		self.line = []   	# array of tune lines as Line

		if filename:
			f = open(filename, 'Ur')
			self.parse(f.read())
			f.close()

	def field(self, field):
		"""
		Returns an information field (e.g., "T", "X"), or None if the given field
		doesn't exist.
		"""
		if field in self._fields:
			return self._fields[field]
		else:
			return None

	def parse(self, str):
		"""
		Parses the given input ABC string.
		"""
		lineBuffer = ''
		lines = str.split('\n')

		for line in lines:

			# Strip superfluous characters.
			line = re.sub('%.*$', '', line) # Strip comments.
			line = line.lstrip().rstrip()   # Strip whitespace.

			# Ignore blank lines.
			if len(line) == 0:
				continue

			# If the lines begins with a letter and a colon, it's an information
			# field. Extract it.
			matches = re.match('([A-Za-z]):\s*(.*)', line)
			if matches:
				#(0) matches the whole regular expression.
				#(1) matches the first pattern.
				#(2) matches the second pattern,etc. 
				self._parseInformationField(matches.group(1), matches.group(2))
			else:
				# We have a tune line.
				if line[-1] == "\\":
					# The current line ends with a \, so just store it in the buffer
					# for now.
					lineBuffer += line.rstrip("\\")
				else:
					# The current line does not end with a \, so add it to whatever
					# lines we might have seen previously and parse it.
					lineBuffer += line
					self.text.append(lineBuffer) # Store raw tune line.
					self.line.append(Line(lineBuffer))
					lineBuffer = ''

	def _parseInformationField(self, field, data):
		# Parses an information field. field is a letter, while data is the
		# data following the field identifier. field is converted to uppercase
		# before storage. Only the first occurrence of the field is stored.
		field = field.upper()
		if field not in self._fields:
			self._fields[field] = data
			
	def getFields(self):
		return self._fields

##############################################################################
class Line(object):
	"""
	Represents one line in a tune.

	Properties
	----------
	text
		The raw text that was parsed.
	measure
		An array of Measure objects representing the individual measures
		within the line.
	"""

	def __init__(self, line=None):
		"""
		Takes a text line and parses it.
		"""
		self.text = None 	# raw text of the line
		self.measure = [] 	# array of Measures
		if line:
			self.parse(line)

	def parse(self, line):
		"""
		Parses a line of ABC.
		"""
		self.__init__()
		self.text = line

		# Split the line into measures. Measure symbols are
		# |, |], ||, [|, |:, :|, ::
		measures = re.split('\||\|]|\|\||\[\||\|:|:\||::', line)

		# Remove empty measures (typically at the end of lines).
		for item in measures:
			if len(item.lstrip().rstrip()) == 0:
				measures.remove(item)

		self.measure = [] # array of Measure objects
		for measure in measures:
			newMeasure = Measure()
			newMeasure.parse(measure)
			self.measure.append(newMeasure)

	def __str__(self):
		return self.text

##############################################################################
class Measure(object):
	"""
	Represents one measure of a line of music.

	Properties
	----------
	text
		The raw text of the measure that was parsed.
	item
		An array of MusicItem objects representing the individual items (notes and
		chords) within this measure.
	repeat
		The repeat number for this measure, or None if there is no repeat.
		This only simply repeats, e.g., [1 and [2
	"""

	def __init__(self):
		"""
		Constructor. Builds an empty Measure object.
		"""
		self._reset()

	def parse(self, text):
		"""
		Parses a string of ABC into Notes and Chords.
		"""
		self._reset()
		self.text = text

		match = re.search('\[([12])', self.text)
		if match:
			# First or second repeat.
			self.repeat = int(match.group(1))
			self._pos += len(match.group(0))

		while self._pos < len(self.text):

			if self.text[self._pos].isspace():
				# Ignore whitespace.
				self._pos += 1

			elif self.text[self._pos] == '"':
				# Parse a chord.
				self._parseChord()

			elif self.text[self._pos] in "^=_" or self.text[self._pos].isalpha() or self.text[self._pos] == '#':
				# Found the start of a note.
				self._parseNote()

			else:
				# Skip over anything we don't recognize.
				self._pos += 1

	def _parseChord(self):
		# Parses a chord.
		newChord = Chord()
		chordText = newChord.parse(self.text[self._pos:])
		newChord.beat = self._beat
		self._beat += newChord.duration
		self.item.append(newChord)
		self._pos += len(chordText) + 2 # add 2 to account for the double quotes

	def _parseNote(self):
		# Parses a note.
		newNote = Note()
		noteText, temp1, temp2, temp3 = newNote.parse(self.text[self._pos:])
		newNote.beat = self._beat
		self._beat += newNote.duration
		self.item.append(newNote)
		self._pos += len(noteText)

	def _reset(self):
		# Clears out all data.
		self.item = []		# array of Chords and Notes for this measure
		self.text = None	# raw text of the measure
		self._pos = 0 		# parsing position within the measure
		self.repeat = None	# repeat number (1 or 2)
		self._beat = 1		# current beat (while parsing)

	def __str__(self):
		return self.text

##############################################################################
class MusicItem(object):
	"""
	Abstract base class for "things" that appear in a line of music:
	notes and chords.

	Properties
	----------
	duration
		Length of this item as a float, e.g., 0.25, 1, etc.
	beat
		The beat on which this item occurs (float). Starts at 1.
	text
		The raw text of this item.
	"""

	def __init__(self):
		# Duration of the item as a float, e.g,. 1/4, 1/8, 1/16, 2
		self.duration = 0.0

		# The beat on which this item occurs: 0, 1, 2, etc.
		self.beat = 0.0

		# Raw text from the tune that makes up this item.
		self.text = ''

	def __str__(self):
		return self.text

##############################################################################
class Chord(MusicItem):
	"""
	Represents a chord.
	"""
	def __init__(self):
		super(Chord, self).__init__()

	def parse(self, str):
		"""
		Parses a chord out of the given string. Returns the raw text that
		was parsed from str without the surrounding	double quotes.
		"""
		pos = 0
		if pos < len(str) and str[pos] == '"':
			self.text += str[pos]
			pos += 1
		else:
			raise RuntimeError('Chord does not begin with ".' + str)

		while pos < len(str) and str[pos] != '"':
			self.text += str[pos]
			pos += 1

		if pos < len(str) and str[pos] == '"':
			self.text += str[pos]
			pos += 1
		else:
			raise RuntimeError('Chord does not end with ":' + str)

		# Remove surrounding double quotes.
		self.text = self.text[1:-1]
		return self.text

##############################################################################
#get duration information
class Note(MusicItem):
	"""
	Represents a note.

	Properties
	----------
	prefix
		Optional ^, =, or _
	note
		The note character itself, A, B, etc.
	suffix
		Optional ' or ,
	length
		Optional note length, /4, 2, etc.
	"""
	def __init__(self):
		super(Note, self).__init__()
		self.prefix = None	# optional ^, =, or _
		self.note = None	# note character [A-z]
		self.suffix = None	# optional ' or ,
		self.length = None	# optional length indication
		self.nextNoteDurationPlus = 0.0 # the value that the next note take away, when the current note has < or >
		self.nextNoteDurationFlag = False # whether the next note takes away the value or not

	def parse(self, str, nextNoteDurationPlus = 0.0, nextNoteDurationFlag = False):
		"""
		Parses a note out of the given string. Returns the raw text that
		was parsed from str.
		"""
		self.__init__()
		pos = 0
		
		if str == '#ending':
			self.text = '#ending'
			self.duration = 0
			self.nextNoteDurationPlus = 0.0
			self.nextNoteDurationFlag = False
			return self.text, self.duration , self.nextNoteDurationPlus, self.nextNoteDurationFlag
		
		
		if pos < len(str) and str[pos] in "^=_":
			# Sharp, natural, or flat symbol.
			self.text += str[pos]
			self.prefix = str[pos]
			pos += 1
			
		if pos < len(str) and str[pos].isalpha():
			# Note letter.
			self.text += str[pos]
			self.note = str[pos]
			pos += 1
		else:
			raise RuntimeError('Note does not contain a character: ' + str.__str__())
		
		if pos < len(str) and str[pos] in "',":
			# Note raise or lower an octave.
			self.text += str[pos]
			self.suffix = str[pos]
			pos += 1
			
		while pos < len(str) and str[pos] in "/0123456789><":
			# Note length.
			self.text += str[pos]
			if not self.length:
				self.length = ""
			self.length += str[pos]
			pos += 1

		#turn the note length(string) into a duration(float).
		#given that all data is valid

		slash_count = self.length.__str__().count('/')
		#this dotted-note notation is only defined between two notes of equal length.
		#attention: two notes which are of equal length
		left_count = self.length.__str__().count('<')
		right_count = self.length.__str__().count('>')
		
		
		self.nextNoteDurationFlag = nextNoteDurationFlag
		self.nextNoteDurationPlus = nextNoteDurationPlus
		
		#print(self.length)
		#if it is just a sigle note
		if self.length is None:
			#if the previous note has < or > suffix
			if self.nextNoteDurationFlag == True:
				self.duration = GlobalConstant.nextNoteDurationBase + self.nextNoteDurationPlus
				#print(self.duration)
				
			#if it does not have
			else:
				self.duration = GlobalConstant.nextNoteDurationBase
				#print(self.duration)
			self.nextNoteDurationPlus = 0.0
			self.nextNoteDurationFlag = False
		#if it is a sigle note followed by a number
		elif slash_count ==0 and left_count ==0 and right_count ==0:
			#and if the previous note have < or >
			if self.nextNoteDurationFlag:
				self.duration = float(re.match('[0-9]', self.length).group(0)) + self.nextNoteDurationPlus
			#or it does not have < and >	
			else:
				self.duration = float(re.match('[0-9]', self.length).group(0))
			self.nextNoteDurationPlus = 0.0
			self.nextNoteDurationFlag = False
				
		else:
			#if it has a /
			if slash_count == 1:
				#if it has only a /, without any number
				if re.search('[0-9]', self.length) == None:
					#if the previous note has < or >
					if self.nextNoteDurationFlag == True:
						self.duration = 1/2 + self.nextNoteDurationPlus
					else:
						self.duration = 1/2

				#or if it has a / with numbers
				else:
					nums = re.findall('[0-9]', self.length)
					#if it has two number
					if len(nums) == 2:
						#if the previous note has < or >
						if self.nextNoteDurationFlag == True:
							self.duration = eval(re.match('[0-9]/[0-9]', self.length).group(0)) + self.nextNoteDurationPlus
						else:
							self.duration = eval(re.match('[0-9]/[0-9]', self.length).group(0))

					#if it has only one number
					elif len(nums) == 1:
						#if the case is like /3, it means 1/3
						if re.search('[0-9]/', self.length) == None:
							#if the previous note has < or >
							if self.nextNoteDurationFlag == True:
								#self.duration = eval('1/' + re.search('/[0-9]', self.length).group(0)) + _nextNoteDurationPlus
								self.duration = eval('1/' + nums[0]) + self.nextNoteDurationPlus
							#if it does not have < and >
							else:
								#self.duration = eval('1' + re.search('/[0-9]', self.length).group(0))
								self.duration = eval('1/' + nums[0])
								
						##if the case is like 3/, it means 3/2
						else:
							if self.nextNoteDurationFlag == True:
								self.duration = eval(nums[0] + '/2') + self.nextNoteDurationPlus
							else:
								self.duration = eval(nums[0] + '/2')
							
			
			#if it has more than one /
			elif slash_count > 1:
				if self.nextNoteDurationFlag == True:
					self.duration = GlobalConstant.nextNoteDurationBase / math.pow(2, slash_count) + self.nextNoteDurationPlus
				else:
					self.duration = GlobalConstant.nextNoteDurationBase / math.pow(2, slash_count)
				

			#if it has no /		
			else:
				# if it has also no number
				if re.search('[0-9]', self.length) == None:
					#if the previous note has < or >
					if self.nextNoteDurationFlag == True:
						self.duration = GlobalConstant.nextNoteDurationBase +self.nextNoteDurationPlus
						#print(self.duration)
					#if the previous note does not have
					else:
						self.duration = GlobalConstant.nextNoteDurationBase

				#or if also have one number
				else:
					if self.nextNoteDurationFlag == True:
						self.duration = float(re.search('[0-9]', self.length).group(0)) + self.nextNoteDurationPlus
					# if the previous note does not have < and >
					else:
						self.duration = float(re.search('[0-9]', self.length).group(0))
											
			#if it also has < 
			if left_count != 0:
				takeaway_part = self.duration / math.pow(2, left_count)
				self.duration =  takeaway_part
				self.nextNoteDurationFlag = True
				self.nextNoteDurationPlus = takeaway_part
				

			#or if it also has > 
			elif right_count != 0:
				takeaway_part = self.duration / math.pow(2, right_count)
				self.duration = self.duration + takeaway_part
				self.nextNoteDurationFlag = True
				self.nextNoteDurationPlus = -(takeaway_part)
				
			# if it has no < and >
			else:
				self.nextNoteDurationFlag = False
				self.nextNoteDurationPlus = 0.0
		
		return self.text, self.duration , self.nextNoteDurationPlus, self.nextNoteDurationFlag
