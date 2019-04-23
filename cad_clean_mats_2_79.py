# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#  (c) 2018 Dan Pool (dpdp) parts based on work by meta-androcto  parts based on work by Saidenka, Materials Utils by MichaleW Materials Conversion: Silvio Falcinelli#
import bpy
from bpy import context
#import os
#os.system('cls')

bl_info = {
    "name": "CadMatClean",
    "author": "Dan Pool (dpdp)",
    "version": (0,0,1),
    "blender": (2, 79,0),
    "description": "Merges material base names for meshes imported from some solid modellers",
    "location": "View3D > Object > CadMatClean",    
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

class CadMatClean(bpy.types.Operator):
    """Clean up imported cad materials"""
    bl_idname = "object.cad_mat_clean"
    bl_label = "Clean Cad Mats"
    bl_options = {'REGISTER', 'UNDO'}
    global converted

    @classmethod
    def poll(cls, context):
        return (	(len(context.selected_objects) > 0)
            and  (context.mode == 'OBJECT')	)	
	
    def execute(self, context):
        
        # determine selected material
        sob = context.object.active_material_index
        sslot = context.object.material_slots[sob]
        sname = sslot.name
#        if not '.' in sname:
#            sbase = sname
#            ssuffix = None
#        else:
#            sbase, ssuffix = sname.rsplit('.',1)
        
        for ob in context.scene.objects:
            for slot in ob.material_slots:
                self.fixup_slot(slot, sslot)
        return {'FINISHED'}
    
    def split_name(self, material):
        name = material.name
        
        if not '.' in name:
            return name, None
        
        base, suffix = name.rsplit('.', 1)
        try:
            num = int(suffix, 10)
        except ValueError:
            # Not a numeric suffix
            return name, None
        
        return base, suffix
    
    def fixup_slot(self, slot, sslot):
        if not slot.material:
            return
        sname = sslot.material.name
        sbase, ssuffix = self.split_name(sslot.material)
        base, suffix = self.split_name(slot.material)
        if suffix == ssuffix:
            return

        if base == sbase:
            try:
                base_mat = bpy.data.materials[sname]
            except KeyError:
                print('Base material %r not found' % base)
                return
        
            slot.material = base_mat
    #End Meta Androcto code as included in his addon

def register():
    bpy.utils.register_module(__name__)
    bpy.types.MATERIAL_MT_specials.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.MATERIAL_MT_specials.remove(menu_func)

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(CadMatClean.bl_idname)
	
if __name__ == "__main__":
    register()
