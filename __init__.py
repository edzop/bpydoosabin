
bl_info = {
	"name": "DooSabin",
	"blender": (2, 93, 0),
	"category": "Object",
}

import bpy

from . import ui


classes = (
	ui.OperatorDooSabin,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.VIEW3D_MT_object.append(ui.menu_func)  # Adds the new operator to an existing menu.

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)


