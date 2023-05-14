# Tiny 2D Rig Tools

Tiny 2D Rig Tools is an addon for Blender that assists in the create and Rigging for 2-D Cut-Out style characters with Grease Pencil Objects. A demo of a pre-release version of this addon can be seen at https://www.youtube.com/watch?v=sQ_ZPXVrPsQ
### Features
 - Generate a Basic Human Armature 
 - Automatically Create IKs with Drivers
 - Add Custom Time Offset Properties to control Mouth/Hand Drawings
 - Use 'Turn-Around' to offset Bone Locations in sync with Time Offset
 - Control Panel to Animate Characters

## Generate New Armature
![create_rig](https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/50ea67ab-9148-4060-b4d6-bd2b95ec6422)
1. Open 'Editor' Side Panel
2. Use the 'Create Armature' Operator 
3. Align bones to your character
4. Select a bone to set as your 'Property Bone' 
5. Use Intilize Rig to setup drivers to control rig via 'Control' Panel



## Adding A Custom Time Offset
![add_time_offset](https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/cca2e236-f8dd-43f3-b407-3a3b25a38cfd)
1. Follow Generate New Rig Proceedure
2. Under 'Rig Properties' select Add Custom Property to creae a new Driver Source
3. Under 'Rig Grease Pencil' select 'Add Time Offset with Driver' and select a Property to Drive it

## Editing Turnaround
![edit_turnaround](https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/e5d80b2a-fae7-4fad-ba10-5b7b5c027530)
1. During 'Initilize Rig' ensure Turnaround is Enabled
2. Under Turnaround Editor select `Edit Turnaround Action`
3. Set the position of some bones per frame of turnaround (within turnaround length)
4. Select `Edit Turnaround Action` again to close editor
5. Use `Add OFfset to Selected Bone` to offset bone's location with turnaround information
6. Under Rig Control use Pose and Pose Head to change turnaround position
