# Tiny 2D Rig Tools

Tiny 2D Rig Tools is an addon for Blender that assists in the create and Rigging for 2-D Cut-Out style characters with Grease Pencil Objects. A demo of a pre-release version of this addon can be seen at https://www.youtube.com/watch?v=sQ_ZPXVrPsQ

# Rig Editor
#### Features
 - Generate a Basic Human Armature 
 - Automatically Create IKs with Drivers
 - Add Custom Time Offset Properties to control Mouth/Hand Drawings
 - Use 'Turn-Around' to offset Bone Locations in sync with Time Offset
 - Control Panel to Animate Characters

## Generate New Armature
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/7bf27703-fe3e-46b4-aef3-aafd3acae1a3
1. Open 'Editor' Side Panel
2. Use the 'Create Armature' Operator 
3. Align bones to your character
4. Select a bone to set as your 'Property Bone' 
5. Use Intilize Rig to setup drivers to control rig via 'Control' Panel



## Adding A Custom Time Offset
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/6a985bac-ed46-47b0-954d-fbf69335f2d8

1. Follow Generate New Rig Proceedure
2. Under 'Rig Properties' select Add Custom Property to creae a new Driver Source
3. Under 'Rig Grease Pencil' select 'Add Time Offset with Driver' and select a Property to Drive it

## Editing Turnaround
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/b2119858-bc75-44cb-a4e1-e6255aa4f42e

1. During 'Initilize Rig' ensure Turnaround is Enabled
2. Under Turnaround Editor select `Edit Turnaround Action`
3. Set the position of some bones per frame of turnaround (within turnaround length)
4. Select `Edit Turnaround Action` again to close editor
5. Use `Add OFfset to Selected Bone` to offset bone's location with turnaround information
6. Under Rig Control use Pose and Pose Head to change turnaround position



# Rig Control

## Changing Time Offset Properties
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/50a1bf72-6d3a-4844-8351-30c2c7898d19

1. Find your User Properties listed at the top
2. Adjust property like 'Mouth' to change Iime Offset Position

## Changing Turnaround 
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/65830247-308c-48fe-a948-14b9d97a526c

1. Set a new POST to adjust Body and HEad
2. Use HEAD POSE to adjust just the head

## IK Pole Flipping
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/ff8c8a9d-934b-4cd2-b02a-5d39cd97cd5f

1. Use FLIP Icon to enable IK Pole Flipping
2. IK Pole Flip will enable a transoform modifier on the Pole to adjust it's location

## Bake IK to FK
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/1ded699f-aca8-433c-997b-2ce381ad08f9

1. Set IK to desired ocation
2. Use Disable IK Button to Bake the exact location to FK
3. FK adjustments can now be made

**NOTE:** Switching back from IK to FK will give inaccurate result as show in above demo

## Nudge Limb Chain
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/945987bd-4ea8-4349-a839-50f64333ea8a

1. Use '- Back' to move limb chain behind character
2. use '+ Forward' to move limb chain infront of character

## Controlling Hands
https://github.com/NickTiny/Tiny-2D-Rig-Tools/assets/86638335/ce175c7c-af37-4b7f-a028-d971897110a0

1. Use 'ARROW' to Nudge hand infront on Limb Chain
2. Select a Hand Time Offset integer to change hand pose
3. Use the 'MIRROR' icon to Flip the Drawing
