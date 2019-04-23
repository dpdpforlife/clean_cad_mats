# Clean Cad Mats
*Merge duplicate materials.*

This is a simple addon for merging like named materials. This serves a common need for imported cad data. I often ran into issues with large assemblies imported into Blender where I may have hundreds of bolts each with a unique material (bolt_mat.001, bolt_mat.002, bolt_mat.003, bolt_mat.004, bolt_mat.005, bolt_mat.006, etc.) whereas in the cad software the model originated in, these were all a single material that could be edited one time and all instances of the bolt_mat would be updated. Manually reasigning hundreds of materials proved to be very time consuming. 

With Clean Cad Maps, you can choose which version of the material to keep and replace all materials that have the same base name. For instance in the image below, selecting Mat.004 in the material properties tab and choosing Clean Cad Mats from the Material Specials menu (which is called the Material Context menu in Blender 2.80) will replace all materials in the scene with the base name "Mat" (Mat.001, Mat.894, etc.) with the Mat.004 material.

![Clean Cad Mats](https://i.ibb.co/ngSRysB/Clean-Cad-Mats.png)


As seen below, the addon works in a similar manner in Blender 2.79.


![Clean Cad Mats](https://i.ibb.co/SKMBbq4/Clean-Cad-Mats.png)

To install the addon, download the version that works with your Blender version by right clicking the clean_cad_mats_2_xx.py file and choosing save as. 

![Download](https://i.ibb.co/vQgp6gW/Download-Addon.png)
