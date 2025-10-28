The original README is included here for reference:

[![Original](https://img.shields.io/badge/Original%20README-blue)](https://github.com/yifanye2015/pyroms/blob/main/README-original.md)

# Pyroms
Note: this is still a work in progress! A user guide will eventually be written up after everything has been tested. Any *italicised* text are comments for my own use and can be ignored.

This project is a fork of the original Pyroms repo at [ESMG/pyroms](https://github.com/ESMG/pyroms). This version contains both new and modified scripts aimed at simplifying the setup process and reducing the need to perform manual changes to the code, so that new users can get Pyroms running with minimal fuss. The core functionalities remain unchanged. 

This version is suitable for Python 3.8.

## Resources
The [ROMS tutorial](https://www.youtube.com/playlist?list=PLBPoOsxO35OpUFOMoDUUcxf_XKXo-ugKY) on YouTube by Yusri Yusup (without which this project would not be possible) provides a step-by-step demonstration to get Pyroms and ROMS running.

## Prerequisites
Pyroms must be installed on a Linux machine; Ubuntu and WSL are recommmended. This version requires [Anaconda](https://www.anaconda.com/) to be installed. The workflow also uses GridBuilder, which is a Windows application that can be downloaded [here](https://austides.com/downloads/).

## Installation (untested)
To clone a copy of the source and install the pyroms packages, you can use the following commands
```
# Cd to a convenient directory (e.g. home directory ~/)
$ git clone https://github.com/yifanye2015/pyroms.git
$ cd pyroms/test_pyroms
$ ./setup_conda_env_pyroms.sh
# This sets up the requisite conda environment

# Cd back to that convenient directory (~/)
$ pip install -e pyroms/pyroms
$ pip install -e pyroms/pyroms_toolbox
$ pip install -e pyroms/bathy_smoother
```

### Install SCRIP (untested)
This is needed to unlock all functionalities.
```
# Start in that convenient directory into which you cloned pyroms.
# Cd to the SCRIP source directory.
$ cd pyroms/pyroms/external/scrip/source/

# Print the location of the active Conda environment.
# The active environment location is used to find the netCDF and
# other libraries.
$ conda info | grep "active env location"
    active env location : /home/hadfield/miniconda3/envs/python38

# Run make to build the scrip Python extension and install it into the Conda
# environment. The makefile calculates a variable called SCRIP_EXT_DIR, into
# which it installs the scrip Python extension. If pyroms has been installed
# in editable (development) mode, set the DEVELOP variable to a non-empty value.
$ export PREFIX=/home/hadfield/miniconda3/envs/python38
$ make DEVELOP=1 PREFIX=$PREFIX install
$ mv -vf scrip*.so ../../../pyroms
‘scrip.cpython-38-x86_64-linux-gnu.so’ -> ‘../../../pyroms/scrip.cpython-38-x86_64-linux-gnu.so’
```
(*should write a script to do this*)

## Using Pyroms
### Creating the ROMS grid for the region of interest with GridBuilder and Google Maps
First, select the region of interest in GridBuilder, and generate the ROMS grid while noting down some grid parameters listed below (a guide can be found [here](https://austides.com/wp-content/uploads/GridBuilder-v0.99.pdf)). 

GridBuilder parameters to be noted down during grid creation:
- L (xi), M (eta)
- N (levels), Vtransform, theta_s, theta_m, tcline

Next, using Google Maps, mark out a rectangular region that completely encompasses the ROMS grid, and note down the latitudes and longitudes of the corners (*include pictures*). 

### Creating a new project
*A script which will do the setup automatically will be made eventually*
There are two template directories in the top pyroms directory: test_pyroms and test_MERRA2. test_pyroms processes HYCOM files to produce boundary, climate, and initial condition files, and test_MERRA2 processes MERRA-2 files to produce forcing files. All necessary scripts and subdirectories are in the template directories and should not be changed. 

To create a new project, simply duplicate the template directories and rename them (e.g. my_project_name_hycom and my_project_name_merra) (*need better template dir names*):
```
cp test_pyroms my_project_name_hycom
cp test_MERRA2 my_project_name_merra
```

From here on, make sure the previously set up conda environment is activated (*will include code to check this at runtime*).
### HYCOM data
First, move the file created by GridBuilder into test_pyroms.
In test_pyroms, open `config.env`, and change/update these variables (do not use spaces):
- PROJECT_NAME (choose a memorable name such as penang_2019)
- YEAR (year to be analysed) (*might allow year ranges in the future*)
- GRIDBUILDER_NAME (name of the file created from GridBuilder)
- GRIDBUILDER_PATH (the full path to the GridBuilder file; can use `pwd` to get the path to test_pyroms and append the filename to it)
- GB_L, GB_M, THETA_S, THETA_B, TCLINE (GridBuilder parameters)
- MAP_LAT_SOUTH, MAP_LAT_NORTH, MAP_LON_WEST, MAP_LON_EAST (coordinates of region from Google Maps)
- GRID_N, GRID_TYPE, GRID_VTRANS, GRID_THETA_S, GRID_THETA_B, GRID_TCLINE (also GridBuilder parameters, *will fix this duplication eventually*)
- HYCOM_START_DATE, HYCOM_END_DATE (date range to analyse)
Save the file.

Extra step: for the first run, go into `run_pyroms_hycom.sh`, uncomment `python3 update_gridid.py` and save the file. For subsequent runs, keep that line commented out unless there are any changes to the GridBuilder grid. (*probably add a flag in the future to only activate it if requested*)

Run all scripts with
```
./run_pyroms_hycom.sh
```

Python scripts can also be run individually; ensure `source config.env` is run before that.

### MERRA-2 data
First, go to [NASA Earthdata](https://urs.earthdata.nasa.gov) to create an account, and note down your username and password. Then, cd to test_MERRA2.

Extra step: duplicate the `config.env` file from test_pyroms to test_MERRA2 (*will eventually consolidate into a single config.env somewhere*), and update these variables:
- EARTHDATA_USERNAME, EARTHDATA_PASSWORD (*will change this to use .netrc when I eventually figure it out*)
- MERRA2_START_DATE, MERRA2_END_DATE (date range to analyse)
Save the file.

Run all scripts with
```
./get_MERRA_Forcings_from_nasa_opendap_3hours.bash
```

Python scripts can also be run individually; ensure `source config.env` is run before that, and run `./add_coordinates_attribute.bash` after that.

Boundary, climate, initial condition, forcing files are successfully generated.
