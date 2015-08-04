import xml.etree.ElementTree as etree
import csv
import argparse
import os
import os.path
import shutil

def create_set(d, cards):
	root = etree.Element("set")
	
	root.set("name", d["name"])
	root.set("id", d["setid"])
	root.set("gameId", d["gameid"])
	root.set("gameVersion", d["gameversion"])
	root.set("version", d["version"])
	
	etree.SubElement(root, "packaging")
	etree.SubElement(root, "markers")
	cxml = etree.SubElement(root, "cards")
	
	for card in cards:
		create_card(cxml, card)
	
	return etree.ElementTree(root)
	

def create_card(parent, cardinfo):
	c = etree.SubElement(parent, "card")
	
	for name, value in cardinfo.items():
		if name == 'name':
			c.set("name", value)
		elif name == 'guid':
			c.set("id", value)
		elif name == 'id':
			create_prop(c, "Collector Info", "F" + value)
		else:
			create_prop(c, name, value)
			
	create_prop(c, "AutoScript", "")
	create_prop(c, "AutoAction", "")
	create_prop(c, "Instructions", "")
		
def create_prop(elem, name, value):
	e = etree.SubElement(elem, "property")
	e.set("name", name)
	e.set("value", value)
	

def create_arg_parser():
	p = argparse.ArgumentParser(description="Stuff")
	p.add_argument('--setid')
	p.add_argument('--gameid', default='43054c18-2362-43e0-a434-72f8d0e8477c')
	p.add_argument('--name')
	p.add_argument('--gameversion', default='3.1.0.1')
	p.add_argument('--version', default='3.0.0.1')
	p.add_argument('--datafile')
	
	return p
	
def indent(elem, level=0, more_sibs=False):
    i = "\n"
    if level:
        i += (level-1) * '  '
    num_kids = len(elem)
    if num_kids:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
            if level:
                elem.text += '  '
        count = 0
        for kid in elem:
            indent(kid, level+1, count < num_kids - 1)
            count += 1
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            if more_sibs:
                elem.tail += '  '
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            if more_sibs:
                elem.tail += '  '	
				
if __name__ == '__main__':
	arg_parser = create_arg_parser()
	args = vars(arg_parser.parse_args())
	
	shutil.rmtree(args['gameid'], True)
	
	pth = [args['gameid'], "Sets", args['setid'], "Cards"]
	setpth = pth[:3] + ["set.xml"]
	
	os.makedirs(os.path.join('.', *pth))
	
	with open(args['datafile']) as csvfile:
		c = csv.DictReader(csvfile)
	
		s = create_set(args, c)
		indent(s.getroot())
		s.write( os.path.join('', *setpth), xml_declaration=True, encoding="utf-8")
	
