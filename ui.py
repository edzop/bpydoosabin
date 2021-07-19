import bpy

from . import doosabin

from bpy.props import (
		EnumProperty,
		FloatProperty,
		BoolProperty,
		IntProperty
		)


class OperatorDooSabin(bpy.types.Operator):
	"""DooSabin"""      # Use this as a tooltip for menu items and buttons.
	bl_idname = "object.doosabin"        # Unique identifier for buttons and menu items to reference.
	bl_label = "DooSabin"         # Display name in the interface.
	bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


	iterations: IntProperty(
		name="Iterations",
		description="Iterations for doo sabin operator",
		default=1,
		min=1,
		max=10
		)

	gen_face_faces: BoolProperty(
		name="Face Faces",
		description="Generate face-faces",
		default=True
		)

	gen_vert_faces: BoolProperty(
		name="Vert Faces",
		description="Generate vert-faces",
		default=False
		)

	gen_edge_faces: BoolProperty(
		name="Edge Faces",
		description="Generate edge-faces",
		default=True
		)

	hide_source_object: BoolProperty(
		name="Hide source object",
		description="Makes original source object hidden",
		default=False
		)


	def draw(self, context):
		layout = self.layout
		layout.label(text="Generate:")
		layout.prop(self, "gen_face_faces")
		layout.prop(self, "gen_vert_faces")
		layout.prop(self, "gen_edge_faces")
		layout.prop(self, "iterations")
		layout.prop(self, "hide_source_object")

	def execute(self, context):        # execute() is called when running the operator.

		selected_object = bpy.context.object

		if selected_object==None:
			print("No object selected")
			return 0

		my_doosabin = doosabin.doosabin()

		my_doosabin.generate_edge_faces=self.gen_edge_faces
		my_doosabin.generate_vert_faces=self.gen_vert_faces
		my_doosabin.generate_face_faces=self.gen_face_faces
		my_doosabin.hide_source_object=self.hide_source_object

		my_doosabin.perform_doo_sabin(selected_object,self.iterations)

		print("doo sabin finished")

		return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
	self.layout.operator(OperatorDooSabin.bl_idname)
