
# Original copyright notice from:
# https://blenderartists.org/t/doo-sabin-subdivision-script-now-available/334641
# +--------------------------------------------------------+
# | Copyright (c) 2005 Anthony D'Agostino                   |
# | http://www.redrival.com/scorpius                        |
# | scorpius@netzero.com                                    |
# | April 30, 2005                                          |
# | Released under the Blender Artistic Licence (BAL)       |
# +---------------------------------------------------------+
# | Doo-Sabin Subdivision                                   |
# +---------------------------------------------------------+

# Modified for blender 2.93 on July 2021

bl_info = {
	"name": "DooSabin",
	"blender": (2, 93, 0),
	"category": "Object",
}

import bpy
import bmesh

# =========================================
# from mesh tools
# =========================================

def vavg(vlist):

	#print("Returns the average of a list of vectors:")
	#print(vlist)
	x = sum([vec[0] for vec in vlist]) / len(vlist)
	y = sum([vec[1] for vec in vlist]) / len(vlist)
	z = sum([vec[2] for vec in vlist]) / len(vlist)
	#print("average: %f %f %f ======="%(x,y,z))
	
	return (x,y,z)

# =============================
# === Calculate Face Center ===
# =============================
def centroid(verts, face):
	if len(face) < 3: 
		print("Centroid Error, numverts =", len(face))

	return vavg([verts[i] for i in face])

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


# ======================================
# === Doo Sabin Subivision Functions ===
# ======================================
def left_shift(seq):
	val=seq[1:] + seq[0:1]
	#print("left shift: %s -> %s"%(str(seq),str(val)))
	return val

def right_shift(seq):
	val=seq[-1:] + seq[0:-1]
	#print("right shift: %s -> %s"%(str(seq),str(val)))
	return val

def doo_sabin3(verts, faces,depth):
	numfaces = len(faces)
	face_faces = []
	etab = {}

	vert_mapping={}

	for i in range(numfaces):
		print("===== Face: %d ========"%i)
		T = centroid(verts, faces[i])
		numverts = len(faces[i])
		faceverts = [verts[j] for j in faces[i]]
		
		print("faceverts: %s"%str(faceverts))
		
		edge_zip = zip(faceverts, left_shift(faceverts))

		edges=[]
		edge_centers=[]

		for i,(v0,v1) in enumerate(edge_zip):
			edge_center=vavg([v0,v1])
			edges.append([v0,v1])
			edge_centers.append(edge_center)
			print("Edge %d: %s %s - Center: %s"%(i,str(v0),str(v1),str(edge_center)))
			
		print("======")

		centeroids = [T]*numverts
		#v = faceverts
		#w = edge_centers
		rs_edge_centers = right_shift(edge_centers)

		fverts = zip(centeroids,faceverts,edge_centers,rs_edge_centers)

		new_fverts=[]
		for fv in fverts:
			original_vert=fv[1] # second position is original vert
			fv_average=vavg(fv)
			new_fverts.append(fv_average)

			# Add Vert mappings

			vert_key=(original_vert[0],original_vert[1],original_vert[2])

			if vert_key in vert_mapping:
				vert_mapping[vert_key].append(fv_average)
			else:
				vert_mapping[vert_key]=[ fv_average ]

		print("newverts: %s"%(str(new_fverts)))

		#fverts = map(vavg, fverts)

		face_faces.append(new_fverts)

		new_edges = zip(new_fverts,left_shift(new_fverts))

		for i,edge in enumerate(new_edges):
			print("newedge %d: %s"%(i,str(edge)))

			PA=edge[0]
			PB=edge[1]

			sv=edges[i][0]
			ev=edges[i][1]

			evsv_key=( tuple(ev),tuple(sv) )
			svev_key=( tuple(sv),tuple(ev) )

			if evsv_key in etab: 
				#etab[(tuple(ev),tuple(sv))].extend([PB,PA])
				etab[evsv_key].append((PB,PA))
			else:
				etab[svev_key]=[(PB,PA)]

			#new_edge_set.append( [sv,PA])
			#new_edge_set.append([sv,ev])
			#new_edge_set.append([PA,PB])

		#fverts = zip(fverts, left_shift(fverts))

		edge_faces2=[]
		
		print("ETAB")
		for i,e in enumerate(etab):
			val=etab.get(e)
			print("etab %d: %s -> %s"%(i,str(e),str(val)))
			
			if len(val)==2:
				#print(val[0])

				this_face=[ 
					val[0][0], 
					val[0][1], 
					val[1][0],
					val[1][1]
				]

				print("TF1 %d: %s"%(i,str(this_face)))
				edge_faces2.append(this_face)


				this_face=[ 
					val[0][0], 
					val[0][1], 
					val[1][0],
					val[1][1]
				]

				#print("TF2 %d: %s"%(i,str(this_face)))
				#edge_faces2.append(this_face)

				#new_edge_set.append([val[0][0],val[0][1]])
				#new_edge_set.append([val[1][0],val[1][1]])

				#new_edge_set.append([val[1][0],val[0][1]])
				#new_edge_set.append([val[0][0],val[1][1]])

		#edge_faces3=list(map(esort,edge_faces2))
				
				
	#edge_faces = etab.values()
	#vert_faces = make_vfaces(etab)

	#for e in edge_faces:
	#	print(e)
	#	print(len(e))


	#	if len(e)==2:
	#		edge_faces2.append(
	#			[ e[0][0],e[0][1],e[1][0],e[1][1] ]
	#		)

	#edge_faces = [rawface for rawface in edge_faces if len(rawface) > 2]
	#vert_faces = [rawface for rawface in vert_faces if len(rawface) > 2]
	
	#raw_faces = face_faces + vert_faces + edge_faces
	raw_faces = face_faces + edge_faces2

	# ======= Add Corner Faces
	for original_vert,vert_mappings in vert_mapping.items():
		new_corner_face=[]
		#print("original_map: %s"%str(original_vert))
		for mapped_vert in vert_mappings:
			#print(mapped_vert)
			new_corner_face.append(mapped_vert)

		#new_corner_face.reverse()
		#ss=esort(new_corner_face)
		#new_corner_face.reverse()

		if len(new_corner_face)>2:
			
			#if len(new_corner_face)==4:
			#	new_corner_face=[
			#		vert_mappings[3],
			#		vert_mappings[1],
			#		vert_mappings[2],
			#		vert_mappings[0]
			#		]
			
			

			raw_faces.append(new_corner_face)

			#sorted=map(esort,new_corner_face)
			#raw_faces.append(new_corner_face)
			print("new corner: %s"%new_corner_face)


	#print("Vert Mapping: ============")
	#print(vert_mapping)

	if depth==1: 
		#print("Raw Faces: %s"%str(raw_faces))
		return (raw_faces)

	verts, faces = raw_to_indexed(raw_faces)

	return 	doo_sabin3(verts, faces, depth-1)


class OperatorDooSabin(bpy.types.Operator):
	"""DooSabin"""      # Use this as a tooltip for menu items and buttons.
	bl_idname = "object.doosabin"        # Unique identifier for buttons and menu items to reference.
	bl_label = "DooSabin"         # Display name in the interface.
	bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

	def execute(self, context):        # execute() is called when running the operator.

		selected_object = bpy.context.object

		if selected_object==None:
			print("No object selected")
			return 0

		me = selected_object.data
		bm_old = bmesh.new()         # Create a new bmesh container instance
		bm_old.from_mesh(me)         # Pass your mesh into this container

		verts=[]
		faces=[]
		edges=[]

		for v in bm_old.verts:
			verts.append( [ v.co[0],v.co[1],v.co[2] ] )

		for e in bm_old.edges:
			edges.append( [e.verts[0].index,e.verts[1].index ] )

		for f in bm_old.faces:
			this_face=[]
			for v in f.verts:
				this_face.append(v.index)

			faces.append(this_face)
		
		#print("verts:")
		#print(verts)

		#print("faces:")
		#print(faces)

		#print("edges:")
		#print(edges)
		
		raw_faces=doo_sabin3(verts,faces,1)
#		raw_faces=doo_sabin2(verts,faces,1)


		# Create New Mesh
		bm_new = bmesh.new()         # Create a new bmesh container instance

		# ============== recreate =============
		#print("\n----- raw faces:")
		#print(raw_faces)

		for i,face in enumerate(raw_faces):
			#print("Face %d: %s --------------"%(i,face))

			newverts=[]

			for i2,v in enumerate(face):
				#print("vert %d: %s"%(i2,v))

				new_vert=bm_new.verts.new(v)
				newverts.append(new_vert)

			bm_new.faces.new(newverts)

		#for edgeset in new_edge_set:

		#	v1=bm_new.verts.new(edgeset[0])
		#	v2=bm_new.verts.new(edgeset[1])
		#	bm_new.edges.new([ v1,v2 ])


		mesh_data = bpy.data.meshes.new("cloned")

		bm_new.to_mesh(mesh_data)

		mesh_obj = bpy.data.objects.new(mesh_data.name, mesh_data)

		# Shift position to visualize old vs new better
		mesh_obj.location.x=selected_object.location.x+2
		mesh_obj.location.y=selected_object.location.y-2

		bpy.context.collection.objects.link(mesh_obj)

		print("doo sabin finished")

		return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
	self.layout.operator(OperatorDooSabin.bl_idname)

def register():
	bpy.utils.register_class(OperatorDooSabin)
	bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
	bpy.utils.unregister_class(OperatorDooSabin)

