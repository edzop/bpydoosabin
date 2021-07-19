# +---------------------------------------------------------+
# | Copyright (c) 2001 Anthony D'Agostino                   |
# | http://www.redrival.com/scorpius                        |
# | scorpius@netzero.com                                    |
# | March 27, 2001                                          |
# +---------------------------------------------------------+
# | Vector Functions                                        |
# +---------------------------------------------------------+


def vavg(vlist):

	#print("Returns the average of a list of vectors:")
	#print(vlist)
	x = sum([vec[0] for vec in vlist]) / len(vlist)
	y = sum([vec[1] for vec in vlist]) / len(vlist)
	z = sum([vec[2] for vec in vlist]) / len(vlist)
	#print("average: %f %f %f ======="%(x,y,z))
	
	return (x,y,z)
