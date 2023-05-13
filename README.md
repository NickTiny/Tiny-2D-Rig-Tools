# Tiny 2D Rig Tools

Tiny 2D Rig Tools is an addon for Blender that assists in the create and Rigging for 2-D Cut-Out style characters with Grease Pencil Objects. A demo of a pre-release version of this addon can be seen at https://www.youtube.com/watch?v=sQ_ZPXVrPsQ
### Features
 - Generate a Basic Human Armature 
 - Automatically Create IKs with Drivers
 - Add Custom Time Offset Properties to control Mouth/Hand Drawings
 - Use 'Turn-Around' to offset Bone Locations in sync with Time Offset
 - Control Panel to Animate Characters

 ### Usage
 1. Clone Repository and Add as Addon
 2. Use Create Rig to generate a new Rig
 3. Use Intilize Rig to Add Drivers
 4. Use Rig Grease Pencil to attach GPs to Armature

### Generate New Rig

1. Open a blank .blend file
2. Open 'Editor' Side Panel
3. Use the 'Create Armature' Operator 
5. Align bones to 
6. Select a bone to set as your 'Property Bone' 
7. Use Intilize Rig to control rig with 'Control' Panel

### Adding A Custom Time Offset
1. Follow Generate New Rig Proceedure
2. Under 'Rig Properties' select Add Custom Property to creae a new Driver Source
3. Under 'Rig Grease Pencil' select 'Add Time Offset with Driver' and select a Property to Drive it

### Editing Turnaround
1. During 'Initilize Rig' ensure Turnaround is Enabled
2. Under Turnaround Editor select `Edit Turnaround Action`
3. Set the position of some bones per frame of turnaround (within turnaround length)
4. Select `Edit Turnaround Action` again to close editor
5. Use `Add OFfset to Selected Bone` to offset bone's location with turnaround information
6. Under Rig Control use Pose and Pose Head to change turnaround position

### Editor
![image](https://github.com/NickTiny/tiny_2d_rig_tools/assets/86638335/a5864134-372b-42da-b563-c1eb403285ba)

### Control Panel
![image](https://github.com/NickTiny/tiny_2d_rig_tools/assets/86638335/8d321511-2f70-4d46-8f68-750e02b949c5)
