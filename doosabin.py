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

# Modified for blender 2.93 on July 2021 by edzop


import bpy
import bmesh

from . import meshtools
from . import vector

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


class doosabin:

    debug_output=True
    generate_vert_faces=True
    generate_edge_faces=True
    generate_face_faces=True

    averaging_weight=1.0

    hide_source_object=True

    def doo_sabin3(self,verts, faces,depth):

        numfaces = len(faces)
        etab = {}
        raw_faces=[]
        vert_mapping={}

        for i in range(numfaces):
            face_faces=[]
            print("===== Face: %d ========"%i)
            T = meshtools.centroid(verts, faces[i])
            numverts = len(faces[i])
            faceverts = [verts[j] for j in faces[i]]
            
            print("faceverts: %s"%str(faceverts))
            
            edge_zip = zip(faceverts, left_shift(faceverts))

            edges=[]
            edge_centers=[]

            for i,(v0,v1) in enumerate(edge_zip):

                if self.averaging_weight!=0:
                    vAverage=[ v0[0]*self.averaging_weight,v0[1]*self.averaging_weight,v0[2]*self.averaging_weight ]
                    edge_center=vector.vavg([v0,v1,vAverage])
                else:
                    edge_center=vector.vavg([v0,v1])
                edges.append([v0,v1])
                edge_centers.append(edge_center)
                
                if self.debug_output:
                    print("Edge %d: %s %s - Center: %s"%(i,str(v0),str(v1),str(edge_center)))
                
            print("======")

            centeroids = [T]*numverts
            rs_edge_centers = right_shift(edge_centers)

            fverts = zip(centeroids,faceverts,edge_centers,rs_edge_centers)

            new_fverts=[]
            for fv in fverts:
                original_vert=fv[1] # second position is original vert
                fv_average=vector.vavg(fv)
                new_fverts.append(fv_average)

                # Add Vert mappings

                vert_key=(original_vert[0],original_vert[1],original_vert[2])

                if vert_key in vert_mapping:
                    vert_mapping[vert_key].append(fv_average)
                else:
                    vert_mapping[vert_key]=[ fv_average ]

            if self.debug_output:
                print("newverts: %s"%(str(new_fverts)))

            face_faces.append(new_fverts)

            if self.generate_face_faces:
                raw_faces.extend(face_faces)

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

        if self.generate_edge_faces:

            edge_faces=[]

            for i,e in enumerate(etab):
                
                val=etab.get(e)
                print("etab %d: %s -> %s"%(i,str(e),str(val)))
                
                if len(val)==2:

                    this_face=[ 
                        val[0][0], 
                        val[0][1], 
                        val[1][0],
                        val[1][1]
                    ]

                    print("TF1 %d: %s"%(i,str(this_face)))
                    edge_faces.append(this_face)


                    # This is helpful for drawing lines to show how vertices are being constructed
                    #new_edge_set.append([val[0][0],val[0][1]])
                    #new_edge_set.append([val[1][0],val[1][1]])

                    #new_edge_set.append([val[1][0],val[0][1]])
                    #new_edge_set.append([val[0][0],val[1][1]])

            print("appending: %s"%edge_faces)

            raw_faces.extend(edge_faces)
                
                    
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
        
        if self.generate_vert_faces:

            # ======= Add Corner Faces
            for original_vert,vert_mappings in vert_mapping.items():
                new_vert_face=[]
                #print("original_map: %s"%str(original_vert))
                for mapped_vert in vert_mappings:
                    new_vert_face.append(mapped_vert)

                #new_vert_face.reverse()
                #ss=esort(new_vert_face)
                #new_vert_face.reverse()

                if len(new_vert_face)>2:
                    
                    #if len(new_vert_face)==4:
                    #	new_vert_face=[
                    #		vert_mappings[3],
                    #		vert_mappings[1],
                    #		vert_mappings[2],
                    #		vert_mappings[0]
                    #		]
                    
                    

                    raw_faces.append(new_vert_face)

                    #sorted=map(esort,new_vert_face)
                    #vert_faces.append(new_vert_face)
                    print("new corner: %s"%new_vert_face)


        #print("Vert Mapping: ============")
        #print(vert_mapping)

        verts, faces = meshtools.raw_to_indexed(raw_faces)

        if depth==1: 
            #print("Raw Faces: %s"%str(raw_faces))
            return verts, faces

        return 	self.doo_sabin3(verts, faces, depth-1)

    def build_new_mesh(self,verts,faces,new_object_name):

        # Create New Mesh
        bm_new = bmesh.new()

        if self.debug_output:
            print("verts:")
            print(verts)

            print("faces:")
            print(faces)

        # ============== recreate =============
        #print("\n----- raw faces:")
        #print(raw_faces)

        newverts=[]

        for i,vert in enumerate(verts):
            if self.debug_output:
                print("Vert %d: %s"%(i,vert))

            new_vert=bm_new.verts.new(vert)
            newverts.append(new_vert)
        
        for i,f in enumerate(faces):

            faceverts=[]

            if self.debug_output:
                print("Face %d: %s"%(i,f))

            for v in f:
                faceverts.append(newverts[v])

            print("Face Verts")
            print(faceverts)
                
            bm_new.faces.new(faceverts)

        #for edgeset in new_edge_set:
        #	v1=bm_new.verts.new(edgeset[0])
        #	v2=bm_new.verts.new(edgeset[1])
        #	bm_new.edges.new([ v1,v2 ])

        mesh_data = bpy.data.meshes.new(new_object_name)

        bm_new.to_mesh(mesh_data)

        mesh_obj = bpy.data.objects.new(mesh_data.name, mesh_data)

        return mesh_obj


    def perform_doo_sabin(self,selected_object,iterations):
        me = selected_object.data

        old_object_name=selected_object.name

        new_object_name=old_object_name+"_backup"

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

        if self.debug_output:
            print("verts:")
            print(verts)

            print("faces:")
            print(faces)

            print("edges:")
            print(edges)
        
        verts,faces=self.doo_sabin3(verts,faces,iterations)

        mesh_obj=self.build_new_mesh(verts,faces,new_object_name)

        
        mesh_obj.location.y=selected_object.location.y
        mesh_obj.location.z=selected_object.location.z

        if self.hide_source_object:
            selected_object.hide_viewport = True
            selected_object.hide_render = True

            mesh_obj.location.x=selected_object.location.x
        else:
            # Shift position to visualize old vs new better 
            # shift by old object dimension X + 10%
            mesh_obj.location.x=selected_object.location.x+selected_object.dimensions.x+(selected_object.dimensions.x*0.1)



        bpy.context.collection.objects.link(mesh_obj)