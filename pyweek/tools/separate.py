 #!/usr/bin/env python
import inkex
class MyEffect(inkex.Effect):
	def __init__(self):
		   inkex.Effect.__init__(self)
	      def effect(self):
 	       layerNames = ['fore','plat','back']
		  for l in layerNames:
			      path = '//*[@inkscape:layer="%s"]' % l
			    for node in xml.xpath.Evaluate(path,self.document):
 			      layers[l] = node
				  parents[l] = node.parent
				Nodee = MyEffect()e.affect()


		parents['plat'].removeChild(layers['plat'])
		 parents['back'].removeChild(layers['back'])
		    f = open(pathToTempfile, 'w')
		 inkex.xml.dom.ext.Print(self.document, f)
		  f.close()
		   pythonsExecCmd('inkscape --options to export %s' % pathToTempfile)
                parents['fore'].appendChild(layers['fore'])
                parents['back'].appendChild(layers['back'])

