# Analog Clock in Blender

#### Quick start:

- You can run the script in terminal with the following syntax:
    
    `blender --python=*path_to_file*  -- --hours 0-23 --minutes 0-59`

#### Description:

- This script creates analog clock in mesh with variable time inputted by line arguments

- Time can be set in a 24 or 12 hour format. However, the script will not accept parameters over the specified limit


### Line arguments:

- `blender [path_to_blender]` 
    
	- in case blender is not installed on PATH, you can exchange first argument with path to blender

- `--python` 
    
	- blender argument for selecting a path to python file with script

- `--`
   
	- necessary mark for blender to ignore script variables

- `--hours [-h]` 
    
	-  whole number of hours with limit of 24 (excluded), default value 0

- `--minutes [-m]`
    
	- whole number of minutes with limit of 60 (excluded), default value 0

- `--random [-r]`
    
	- ask the script to create hour with random time set
