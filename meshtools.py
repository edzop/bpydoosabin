# $Id: meshtools.py,v 1.5 2004/11/30 02:27:46 ianwill Exp $
#
# +---------------------------------------------------------+
# | Copyright (c) 2001 Anthony D'Agostino                   |
# | http://www.redrival.com/scorpius                        |
# | scorpius@netzero.com                                    |
# | September 28, 2002                                      |
# | Released under the Blender Artistic Licence (BAL)       |
# | Import Export Suite v0.5                                |
# +---------------------------------------------------------+
# | Common Functions & Global Variables For All IO Modules  |
# +---------------------------------------------------------+

from . import vector


# =============================
# === Calculate Face Center ===
# =============================
def centroid(verts, face):
	if len(face) < 3: 
		print("Centroid Error, numverts =", len(face))

	return vector.vavg([verts[i] for i in face])



# ========================
# === Indexed <--> Raw ===
# ========================
def raw_to_indexed(raw_faces):
	Verts = []
	Coords = {}
	Index = 0

	#Faces = map(None, raw_faces)

	# Create blank data structure because above code doesn't work in python 3
	Faces=[]
	for f in raw_faces:
		newface=[]
		for i in range(len(f)):
			newface.append(0)
		Faces.append(newface)

	#Faces = RawTriangles[:] # copy.deepcopy()
	
	for i in range(len(raw_faces)):
		for j in range(len(raw_faces[i])):
			vertex = raw_faces[i][j]
			if vertex not in Coords:
				Coords[vertex] = Index
				Index += 1
				Verts.append(vertex)
			Faces[i][j] = Coords[vertex]

	return (Verts, Faces)
