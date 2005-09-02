#!/usr/bin/env python
"""
inkex.py
A helper module for creating Inkscape extensions
"""
import sys, optparse, re, math
import xml.dom.ext
import xml.dom.ext.reader.Sax2
import xml.xpath

def parseStyle(s):
	"""Create a dictionary from the value of an inline style attribute"""
	return dict([i.split(":") for i in s.split(";")])
def formatStyle(a):
	"""Format an inline style attribute from a dictionary"""
	return ";".join([":".join(i) for i in a.iteritems()])

def lexPath(d):
	"""
	returns and iterator that breaks path data 
	identifies command and parameter tokens
	"""
	offset = 0
	length = len(d)
	delim = re.compile(r'[ \t\r\n,]+')
	command = re.compile(r'[MLHVCSQTAZmlhvcsqtaz]')
	parameter = re.compile(r'(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)')
	while 1:
		m = delim.match(d, offset)
		if m:
			offset = m.end()
		if offset >= length:
			break
		m = command.match(d, offset)
		if m:
			yield [d[offset:m.end()], True]
			offset = m.end()
			continue
		m = parameter.match(d, offset)
		if m:
			yield [d[offset:m.end()], False]
			offset = m.end()
			continue
		#TODO: create new exception
		raise Exception, 'Invalid path data!'
'''
pathdefs = {commandfamily:
	[
	implicitnext,
	#params,
	[casts,cast,cast],
	[coord type,x,y,0]
	]}
'''
pathdefs = {
	'M':['L', 2, [float, float], ['x','y']], 
	'L':['L', 2, [float, float], ['x','y']], 
	'H':['H', 1, [float], ['x']], 
	'V':['V', 1, [float], ['y']], 
	'C':['C', 6, [float, float, float, float, float, float], ['x','y','x','y','x','y']], 
	'S':['S', 4, [float, float, float, float], ['x','y','x','y']], 
	'Q':['Q', 4, [float, float, float, float], ['x','y','x','y']], 
	'T':['T', 2, [float, float], ['x','y']], 
	'A':['A', 7, [float, float, float, int, int, float, float], [0,0,0,0,0,'x','y']], 
	'Z':['L', 0, [], []]
	}
def parsePath(d):
	"""
	Parse SVG path and return an array of segments.
	Removes all shorthand notation.
	Converts coordinates to absolute.
	"""
	retval = []
	lexer = lexPath(d)

	pen = (0.0,0.0)
	subPathStart = pen
	lastControl = pen
	lastCommand = ''
	
	while 1:
		try:
			token, isCommand = lexer.next()
		except StopIteration:
			break
		params = []
		needParam = True
		if isCommand:
			if not lastCommand and token.upper() != 'M':
				raise Exception, 'Invalid path, must begin with moveto.'	
			else:				
				command = token
		else:
			#command was omited
			#use last command's implicit next command
			needParam = False
			if lastCommand:
				if token.isupper():
					command = pathdefs[lastCommand.upper()][0]
				else:
					command = pathdefs[lastCommand.upper()][0].lower()
			else:
				raise Exception, 'Invalid path, no initial command.'	
		numParams = pathdefs[command.upper()][1]
		while numParams > 0:
			if needParam:
				try: 
					token, isCommand = lexer.next()
					if isCommand:
						raise Exception, 'Invalid number of parameters'
				except StopIteration:
		                        raise Exception, 'Unexpected end of path'
			cast = pathdefs[command.upper()][2][-numParams]
			param = cast(token)
			if command.islower():
				if pathdefs[command.upper()][3][-numParams]=='x':
					param += pen[0]
				elif pathdefs[command.upper()][3][-numParams]=='y':
					param += pen[1]
			params.append(param)
			needParam = True
			numParams -= 1
		#segment is now absolute so
		outputCommand = command.upper()
	
		#Flesh out shortcut notation	
		if outputCommand in ('H','V'):
			if outputCommand == 'H':
				params.append(pen[1])
			if outputCommand == 'V':
				params.insert(0,pen[0])
			outputCommand = 'L'
		if outputCommand in ('S','T'):
			params.insert(0,pen[1]+(pen[1]-lastControl[1]))
			params.insert(0,pen[0]+(pen[0]-lastControl[0]))
			if outputCommand == 'S':
				outputCommand = 'C'
			if outputCommand == 'T':
				outputCommand = 'Q'

		#current values become "last" values
		if outputCommand == 'M':
			subPathStart = tuple(params[0:2])
		if outputCommand == 'Z':
			pen = subPathStart
		else:
			pen = tuple(params[-2:])

		if outputCommand in ('Q','C'):
			lastControl = tuple(params[-4:-2])
		else:
			lastControl = pen
		lastCommand = command

		retval.append([outputCommand,params])
	return retval

def formatPath(a):
	"""Format SVG path data from an array"""
	return "".join([cmd + " ".join([str(p) for p in params]) for cmd, params in a])

def translatePath(p, x, y):
	for cmd,params in p:
		defs = pathdefs[cmd]
		for i in range(defs[1]):
			if defs[3][i] == 'x':
				params[i] += x
			elif defs[3][i] == 'y':
				params[i] += y

def scalePath(p, x, y):
	for cmd,params in p:
		defs = pathdefs[cmd]
		for i in range(defs[1]):
			if defs[3][i] == 'x':
				params[i] *= x
			elif defs[3][i] == 'y':
				params[i] *= y

def rotatePath(p, a, cx = 0, cy = 0):
	if a == 0:
		return p
	for cmd,params in p:
		defs = pathdefs[cmd]
		for i in range(defs[1]):
			if defs[3][i] == 'x':
			 	x = params[i] - cx
				y = params[i + 1] - cy
				r = math.sqrt((x**2) + (y**2))
				if r != 0:
					theta = math.atan2(y, x) + a
					params[i] = (r * math.cos(theta)) + cx
					params[i + 1] = (r * math.sin(theta)) + cy

class Effect:
	"""A class for creating Inkscape SVG Effects"""
	def __init__(self):
		self.document=None
		self.selected={}
		self.options=None
		self.args=None
		self.OptionParser = optparse.OptionParser(usage="usage: %prog [options] SVGfile")
		self.OptionParser.add_option("--id",
						action="append", type="string", dest="ids", default=[], 
						help="id attribute of object to manipulate")
	def effect(self):
		pass
	def getoptions(self,args=sys.argv[1:]):
		"""Collect command line arguments"""
		self.options, self.args = self.OptionParser.parse_args(args)
	def parse(self,file=None):
		"""Parse document in specified file or on stdin"""
		reader = xml.dom.ext.reader.Sax2.Reader()
		try:
			try:
				stream = open(file,'r')
			except:
				stream = open(self.args[-1],'r')
		except:
			stream = sys.stdin
		self.document = reader.fromStream(stream)
		stream.close()
	def getselected(self):
		"""Collect selected nodes"""
		for id in self.options.ids:
			path = '//*[@id="%s"]' % id
			for node in xml.xpath.Evaluate(path,self.document):
				self.selected[id] = node
	def output(self):
		"""Serialize document into XML on stdout"""
		xml.dom.ext.Print(self.document)
	def affect(self):
		"""Affect an SVG document with a callback effect"""
		self.getoptions()
		self.parse()
		self.getselected()
		self.effect()
		self.output()


