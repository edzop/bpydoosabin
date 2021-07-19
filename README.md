# bpydoosabin
bpydoosabin is a doo sabin subdivision script for blender.

The [Original Version](https://scorpius.github.io/blender-plugins.htm) was written in 2005 for Blender 2.37.

This version modifies the previous version to work on blender 2.93

Example subdivisions:

![ds1](images/ds1.jpg)

![ds1](images/ds2.jpg)


## Installation
Clone this repository into your `blender/scripts/addons` directory then enable via blender addon preferences. Select an object and press F3 to search for operators. Type or choose doosabin


## Todo

- Add GUI for changing parameters on the fly and adjusting options
- Ability to toggle edge_faces and vert_faces on or off
- Ability to assign material slot index to individual face types.
- Update readme to describe nomenclature for generated face types
- Update bmesh updater to reuse vertex (currently vertices are created for each face and not reused. Currently need to remove doubles after generation until this is fixed)
- Add parameter to adjust weight of vertex to normal averaging to finetune generated geometry. 
- Add automated unit test script to generate several predefined shapes and execute modifier on each one to analyze results. automatically render unit tests for communicating change updates. 