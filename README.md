The original README is included here for reference:

[![Original](https://img.shields.io/badge/Original%20README-blue)](https://github.com/yifanye2015/pyroms/blob/main/README-original.md)

# Pyroms
Note: this is still a work in progress! A user guide will eventually be written up after everything has been tested. Any *italicised* text are comments for my own use and can be ignored.

This project is a fork of the original Pyroms repo at [ESMG/pyroms](https://github.com/ESMG/pyroms). This version contains both new and modified scripts aimed at simplifying the setup process and reducing the need to perform manual changes to the code, so that new users can get Pyroms running with minimal fuss. The core functionalities remain unchanged. 

This version is suitable for Python 3.8.

## Resources
The [ROMS tutorial](https://www.youtube.com/playlist?list=PLBPoOsxO35OpUFOMoDUUcxf_XKXo-ugKY) on YouTube by Yusri Yusup (without which this project would not be possible) provides a step-by-step demonstration to get Pyroms and ROMS running.

## Prerequisites
Pyroms must be installed on a Linux machine (does not work on MacOS); Ubuntu and WSL are recommmended. This version requires [Anaconda](https://www.anaconda.com/) to be installed. The workflow also uses GridBuilder, which is a Windows application that can be downloaded [here](https://austides.com/downloads/). 

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

## Set up conda environment for the first time
In the top level `pyroms/` directory, run
```
./setup_conda_env_pyroms.sh
```
This sets up the necessary conda environment for pyroms to work. Subsequently, run
```
conda activate <environment-name>
```
at the start of every session to activate the conda environment.

## Using Pyroms
### Creating the ROMS grid for the region of interest with GridBuilder and Google Maps
First, select the region of interest in GridBuilder, and generate the ROMS grid while noting down some grid parameters listed below (a guide can be found [here](https://austides.com/wp-content/uploads/GridBuilder-v0.99.pdf)). 

GridBuilder parameters to be noted down during grid creation:
- L (xi), M (eta)
- N (levels), Vtransform, theta_s, theta_m, tcline

Next, using Google Maps, mark out a rectangular region that completely encompasses the ROMS grid, and note down the latitudes and longitudes of the corners (*include pictures*). 

### Creating a new project
This is an overview of the pyroms directory structure:
```
pyroms/
├── setup_conda_env_pyroms.sh
├── environment.yaml
├── start_new_project.sh
├── template_project/
│   ├── hycom_processing/
│   │   └── scripts.py
│   ├── merra2_processing/
│   │   └── scripts.py
│   ├── output_files/
│   │   └── files.nc
│   ├── .env(.template)
│   ├── config.env
│   ├── run_pyroms_hycom.sh
│   └── run_pyroms_merra2.sh
├── examples/
├── pyroms/
├── pyroms_toolbox/
└── bathy_smoother/
```

There is a template directory `template_project` in the top pyroms directory, which contains subdirectories `hycom_processing`, `merra2_processing` and `output_files`. `hycom_processing` contains scripts that process HYCOM files to produce boundary, climate, and initial condition files, and `merra2_processing` contains scripts that process MERRA-2 files to produce forcing files. Processed files can be found in `output_files`.

All necessary scripts and subdirectories are in the template directory and should not be changed. Ideally the only things needed to be run/edited/opened are:
- `setup_conda_env_pyroms.sh` for initial conda setup
- `start_new_project.sh` to create a new project directory
- `.env` for storing login credentials (when a new project is created, `.env.template` will be replaced with `.env` automatically)
- `config.env` for setting project parameters
- `run_pyroms_hycom.sh` and `run_pyroms_merra2.sh` to run the processing scripts
- `output_files` for retrieving processed files

To create a new project, simply run:
```
./start_new_project.sh
```
where you will be prompted for a project name, and the project directory will be created.

From here on, make sure the previously set up conda environment is activated (*will include code to check this at runtime*).
### HYCOM data
First, move the file created by GridBuilder into `hycom_processing` (*might change the location to template_project in the future*).
Next, in `config.env`, change/update these variables (do not use spaces):
- YEAR (year to be analysed) (*might allow year ranges in the future*)
- GRIDBUILDER_NAME (name of the file created from GridBuilder)
- GRIDBUILDER_PATH (the full path to the GridBuilder file; can use `pwd` to get the path to test_pyroms and append the filename to it)
- GB_L, GB_M, THETA_S, THETA_B, TCLINE (GridBuilder parameters)
- MAP_LAT_SOUTH, MAP_LAT_NORTH, MAP_LON_WEST, MAP_LON_EAST (coordinates of region from Google Maps)
- GRID_N, GRID_TYPE, GRID_VTRANS, GRID_THETA_S, GRID_THETA_B, GRID_TCLINE (also GridBuilder parameters, *will fix this duplication eventually*)
- HYCOM_START_DATE, HYCOM_END_DATE (date range to analyse)

Save the file.

For the first run, or if **any** GridBuilder grid parameters/filename/location have been changed in `config.env`, include a `-g` flag to update `gridid.txt`:
```
./run_pyroms_hycom.sh -g
```
For other runs, the `-g` flag may be omitted:
```
./run_pyroms_hycom.sh
```

Python scripts can also be run individually with generated files remaining in `hycom_processing`; ensure `source config.env` is run before that.

### MERRA-2 data
First, go to [NASA Earthdata](https://urs.earthdata.nasa.gov) to create an account, and store your username and password in `.env`. 

In `config.env`, change/update these variables (do not use spaces):
- MERRA2_START_DATE, MERRA2_END_DATE (date range to analyse)

Save the file.

Run all scripts with
```
./run_pyroms_merra2.sh
```

Python scripts can also be run individually with generated files remaining in `merra2_processing`; ensure `source config.env` is run before that, and run `./add_coordinates_attribute.bash` after running the scripts.

Boundary, climate, initial condition, forcing files are successfully generated in `output_files`.
