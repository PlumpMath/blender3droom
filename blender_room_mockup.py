# author : Ashok Prajapati
# objective : create 3D room with objects setup at the different locations, and color them
# date : april 2017

# references :
# http://blender.stackexchange.com/questions/75754/randomize-location-of-multiple-objects
# https://docs.blender.org/api/blender_python_api_2_77_release/info_tips_and_tricks.html
# http://blender.stackexchange.com/questions/5064/how-to-batch-import-wavefront-obj-files
# http://stackoverflow.com/questions/14982836/rendering-and-saving-images-through-blender-python
# http://www.emalis.com/2015/11/blender-python-script-to-create-animation-with-numerous-cubes-randomly-changing-colors-and-going-up-and-down/
# https://forum.processing.org/one/topic/change-the-color-of-an-obj-imported-shape.html
# http://danielhnyk.cz/creating-animation-blender-using-python/
# https://blender.stackexchange.com/questions/24133/modify-obj-after-import-using-python
# https://blender.stackexchange.com/questions/8777/selecting-and-removing-particular-objects
# https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Export_scripts
# https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Materials_and_textures#Textures

# .obj free downloads image resources
# https://www.cgtrader.com/free-3d-models/Furniture/Sofa
# https://resources.blogscopia.com/tag/sofa/

# code to execute in blender text editor :
# filename = "/path/to/directory/blender_room_mockup.py"
# exec(compile(open(filename).read(), filename, 'exec'))

import bpy
from mathutils import Vector
import random
import os
import uuid
import sys
sys.path.append('/home/ashok/.virtualenvs/machine_learning/lib/python3.5/site-packages')
import psycopg2
conn_string = "host='localhost' dbname='mockup' user='ashok' password=''"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
class ThreeDimRoom:
    path_to_obj_dir = '/home/ashok/project/mockupStudio/blender3droom1/objects/'
    # initialize length, breadth and height of the room, and scene context
    def __init__(self, length, breadth, height):
        # database connection and fetch record from the table for the objects location

        cursor.execute("select length from room")
        records = cursor.fetchall()
        for r in records:
            self.length = r[0]
        # self.length = length
        self.breadth = breadth
        self.height = height
        self.scene = bpy.context.scene
        self.context = bpy.context.object

    # room created with archimesh addon
    def create_room(self):
        bpy.ops.mesh.archimesh_room()
        bpy.context.object.RoomGenerator[0].wall_num = 3
        bpy.context.object.RoomGenerator[0].walls[0].w = -self.length
        bpy.context.object.RoomGenerator[0].walls[1].w = self.breadth
        bpy.context.object.RoomGenerator[0].walls[2].w = self.length
        #bpy.context.object.RoomGenerator[0].walls[3].w = -self.breadth
        bpy.context.object.RoomGenerator[0].wall_width = 0.2

        bpy.context.object.RoomGenerator[0].room_height = self.height
        bpy.context.object.RoomGenerator[0].ceiling = True
        bpy.context.object.RoomGenerator[0].floor = True

        # add textures to the wall
        self.create_texture('wall_texture3', '~/Downloads/magnum_beige_03.jpg')

        bpy.data.objects['Room'].location = (4.0,-8.0,0)
        bpy.context.scene.objects.active = bpy.data.objects['Floor']
        self.create_texture('floor_texture', '~/Downloads/wood_floor.jpg')

        # add window
        bpy.ops.mesh.archimesh_window()
        bpy.context.object.WindowObjectGenerator[0].r = 90
        bpy.data.objects['Window_Group'].location = (-12.0, -1.1, 2.0)
        bpy.data.objects['Window_Group'].scale = (2.0, 2.0, 2.0)
        bpy.ops.object.transform_apply(scale=True)

    def create_texture(self, name, texture):
        # Load image file. Change here if the snippet folder is
        # not located in you home directory.
        realpath = os.path.expanduser(texture)
        try:
            img = bpy.data.images.load(realpath)
        except:
            raise NameError("Cannot load image %s" % realpath)

        # Create image texture from image
        cTex = bpy.data.textures.new(name, type='IMAGE')
        cTex.image = img
        # Create material
        mat = bpy.data.materials.new('TexMat%s' %name)

        # Add texture slot for color texture
        mtex = mat.texture_slots.add()
        mtex.texture = cTex
        mtex.texture_coords = 'UV'
        mtex.use_map_color_diffuse = True
        mtex.use_map_color_emission = True
        mtex.emission_color_factor = 0.5
        mtex.use_map_density = True
        mtex.mapping = 'FLAT'

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.unwrap()
        bpy.ops.object.mode_set(mode='OBJECT')

        # Add material to current object
        ob = bpy.context.object
        me = ob.data
        me.materials.append(mat)

    def save_as_image(self):
        image_path = '/home/ashok/project/mockupStudio/images/{}{}'.format(uuid.uuid4(), '.png')
        bpy.data.scenes["Scene"].render.filepath = image_path #self.path_to_save_image_dir
        bpy.ops.render.render(write_still=True)


    def main(self, pattern_id):
        # the main program starts here
        self.create_room()
        cursor.execute('select * from "Configuration" where config_id=%d' % config_id)
        records = cursor.fetchall()

        for r in records:
            if r[2] == sofa:


        # import objects from the directory
        file_list = sorted(os.listdir(self.path_to_obj_dir))
        # get a list of files ending in 'obj'
        obj_list = [item for item in file_list if item.endswith('.obj')]
        # loop through the strings in obj_list and add the files to the scene
        for item in obj_list:
            path_to_file = os.path.join(self.path_to_obj_dir, item)
            bpy.ops.import_scene.obj(filepath=path_to_file)
            # make sure to get all imported objects
            imported_objects = bpy.context.selected_objects[:]
            # define locations statically for each object
            locations_bed = [(-5.0, 1.0, 0.0)]
            locations_sofa = [(-6.0, -5.0, 0.0)]
            locations_leather_sofa =  [(7.0, 9.0, 0.0)]

            # iterate through all objects
            for imp_objects in imported_objects:
                # imp_objects.show_name = True
                # set current object to the active one
                bpy.context.scene.objects.active = imp_objects

                # generate material or color
                mat = bpy.data.materials.new(imp_objects.name)
                r = random.random()
                g = random.random()
                b = random.random()
                mat.diffuse_shader = 'LAMBERT'
                mat.diffuse_intensity = 1.0

                if imp_objects.name.startswith('bed') or imp_objects.name.startswith('mattress') \
                        or imp_objects.name.startswith('Colcha'):
                    imp_objects.location = locations_bed[0]
                    imp_objects.scale = (2.0, 2.0, 2.0)
                    bpy.ops.object.transform_apply(scale=True)

                elif imp_objects.name.startswith('tack'):
                    imp_objects.location = locations_leather_sofa[0]
                    imp_objects.scale = (1.5, 1.5, 1.5)
                    bpy.ops.object.transform_apply(scale=True)

                elif imp_objects.name.startswith('cushion') or imp_objects.name.startswith('big_cushion') \
                        or imp_objects.name.startswith('legs') or imp_objects.name.startswith('sofa_Cube'):
                    imp_objects.location = locations_sofa[0]
                    imp_objects.rotation_euler = (1.57, -0.0, 1.47)
                    imp_objects.scale = (0.75, 0.75, 0.75)
                    bpy.ops.object.transform_apply(scale=True)

                elif imp_objects.name.startswith('Cube'):
                    imp_objects.location = (2.0,3.0,0.0)
                    imp_objects.scale = (0.5, 0.5, 0.5)
                    bpy.ops.object.transform_apply(scale=True)

                else:
                    #imp_objects.location = locations_clear_sofa[0]
                    pass

                mat.diffuse_color = (r, g, b)
                # if a material exists overwrite it
                if len(imp_objects.data.materials):
                    # assign to 1st material slot
                    imp_objects.data.materials[0] = mat

                # if there is no material append it
                else:
                    imp_objects.data.materials.append(mat)
        # IMPORT objects and set locations ends here

        # Add light and set
        lamp_data = bpy.data.lamps.new(name="lamp", type='POINT')
        lamp_object = bpy.data.objects.new(name="Lampicka", object_data=lamp_data)
        self.scene.objects.link(lamp_object)
        lamp_object.location = (0.32, -2.94, 4.37)

        # Set the camera
        #cam_data = bpy.data.cameras.new(name="cam")
        #cam_ob = bpy.data.objects.new(name="Kamera", object_data=cam_data)
        #self.scene.objects.link(cam_ob)
        bpy.data.objects['Camera'].location = (13.65, -3.70, 5.63)
        bpy.data.objects['Camera'].rotation_euler = (1.37, -0.00, 1.35)

        # save the image in the defined path
        self.save_as_image()

        #clear the whole scene for next image
        for ob in bpy.context.scene.objects:
            if ob.name == 'Camera':
                ob.select = False
            else:
                ob.select = True
        # bpy.ops.object.delete()

if __name__ == "__main__":
    # main room
    r = ThreeDimRoom(16.0, 12.0, 6.0)
    r.main(1)
    # for i in range(50):
    #     r.main()

