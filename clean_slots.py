import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty

bl_info = {
    "name": "CleanSlots",
    "author": "Dan Pool (dpdp)",
    "version": (0,0,2),
    "blender": (2, 80,0),
    "description": "Merges material base names for meshes imported from some solid modellers",
    "location": "Properties > Material > Specials > CleanSlots",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

def assignmatslots(ob, matlist):
    #given an object and a list of material names
    #removes all material slots form the object
    #adds new ones for each material in matlist
    #adds the materials to the slots as well.

    scn = bpy.context.scene
    ob_active = bpy.context.active_object
    #scn.objects.active = ob

    for s in ob.material_slots:
        bpy.ops.object.material_slot_remove()

    # re-add them and assign material
    i = 0
    for m in matlist:
        mat = bpy.data.materials[m]
        ob.data.materials.append(mat)
        i += 1

    # restore active object:
    #scn.objects.active = ob_active

def cleanmatslots():
    #check for edit mode
    editmode = False
    actob = bpy.context.active_object
    if actob.mode == 'EDIT':
        editmode = True
        bpy.ops.object.mode_set()

    objs = bpy.context.selected_editable_objects

    for ob in objs:
        if ob.type == 'MESH':
            mats = ob.material_slots.keys()

            #check the polygons on the mesh to build a list of used materials
            usedMatIndex = []  # we'll store used materials indices here
            faceMats = []
            me = ob.data
            for f in me.polygons:
                #get the material index for this face...
                faceindex = f.material_index

                #indices will be lost: Store face mat use by name
                currentfacemat = mats[faceindex]
                faceMats.append(currentfacemat)

                # check if index is already listed as used or not
                found = 0
                for m in usedMatIndex:
                    if m == faceindex:
                        found = 1
                        #break

                if found == 0:
                #add this index to the list
                    usedMatIndex.append(faceindex)

            #re-assign the used mats to the mesh and leave out the unused
            ml = []
            mnames = []
            for u in usedMatIndex:
                ml.append(mats[u])
                #we'll need a list of names to get the face indices...
                mnames.append(mats[u])

            assignmatslots(ob, ml)

            # restore face indices:
            i = 0
            for f in me.polygons:
                matindex = mnames.index(faceMats[i])
                f.material_index = matindex
                i += 1

class VIEW3D_OT_clean_material_slots(bpy.types.Operator):
    """Removes any material slots from selected objects """ \
    """that are not used by the mesh"""
    bl_idname = "view3d.clean_material_slots"
    bl_label = "Clean Material Slots"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        cleanmatslots()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_OT_clean_material_slots)
    bpy.types.MATERIAL_MT_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(CadMatClean)
    bpy.types.MATERIAL_MT_context_menu.remove(VIEW3D_OT_clean_material_slots)

def menu_func(self, context):
    self.layout.operator(VIEW3D_OT_clean_material_slots.bl_idname)
    
if __name__ == "__main__":
    register()
