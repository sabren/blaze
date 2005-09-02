#!/usr/bin/env python 
import inkex2

#a dictionary of all of the xmlns prefixes in a standard inkscape doc
NSS = {u'sodipodi':u'http://inkscape.sourceforge.net/DTD/sodipodi-0.dtd',
u'cc':u'http://web.resource.org/cc/',
u'svg':u'http://www.w3.org/2000/svg',
u'dc':u'http://purl.org/dc/elements/1.1/',
u'rdf':u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
u'inkscape':u'http://www.inkscape.org/namespaces/inkscape'}

class MyEffect(inkex2.Effect):
	def __init__(self):
		inkex2.Effect.__init__(self)
	def effect(self):
		ctx = inkex2.xml.xpath.Context.Context(self.document,processorNss=NSS)
		# all g elements with an inkscape:groupmode attribute that has a value of "layer"
		# that can be found anywhere under the root
		path = '//g[@inkscape:groupmode="layer"]'
		for node in inkex2.xml.xpath.Evaluate(path,self.document, context=ctx):
			print node
			print node.attributes
			#notice the use of the NSS dict again. the namespace uri is required here not the prefix.
			print node.hasAttributeNS(NSS[u'inkscape'],u'groupmode')
			print node.getAttributeNS(NSS[u'inkscape'],u'label')

e = MyEffect()
e.affect()

