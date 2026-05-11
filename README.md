The original README is included here for reference:

[![Original](https://img.shields.io/badge/Original%20README-blue)](https://github.com/yifanye2015/pyroms/blob/main/README-original.md)

# Pyroms
Note: the installation and processing scripts have been verified to work. A proper user guide will eventually be written up. Any *italicised* text are comments for my own use and can be ignored. `Palau_HYCOM` and `test_...` are for testing only and can be ignored.

This project is a fork of the original Pyroms repo at [ESMG/pyroms](https://github.com/ESMG/pyroms). This version contains both new and modified scripts aimed at simplifying the setup process and reducing the need to perform manual changes to the code, so that new users can get Pyroms running with minimal fuss. The core functionalities remain unchanged. 

This version requires both Python 3.8 and Python 3.13+.

## Resources
The [ROMS tutorial](https://www.youtube.com/playlist?list=PLBPoOsxO35OpUFOMoDUUcxf_XKXo-ugKY) on YouTube by Yusri Yusup (without which this project would not be possible) provides a step-by-step demonstration to get Pyroms and ROMS running.

## Prerequisites
Pyroms must be installed on a Linux machine (does not work on MacOS); Ubuntu and WSL are recommmended. This version requires [Anaconda](https://www.anaconda.com/) to be installed. The workflow also uses GridBuilder, which is a Windows application that can be downloaded [here](https://austides.com/downloads/). 

## Installation using scripts
First, install conda on Linux using default options, and run `anaconda3/bin/conda init` from the conda installation location. Restart Ubuntu.

To clone a copy of the source and set up pyroms, you can use the following commands:
```
# Cd to a convenient directory (e.g. home directory ~/)
$ git clone git@github.com:yifanye2015/pyroms.git
$ cd pyroms
$ ./setup_conda_env_py38.bash
$ ./setup_conda_env_opendap_py313.bash
# These set up and activate the requisite conda environments
# The script will also prompt you to install ksh and nco for the pyroms scripts to work
$ sudo apt install ksh nco

# First activate the py38 conda environment
$ conda activate <environment-name>
# Run the SCRIP installer script (this is needed to unlock all functionalities)
$ ./install_scrip.bash
```

## Using Pyroms
### Activating conda
Run `conda activate <environment-name>` at the start of every session to activate the conda environment.

### Creating the ROMS grid for the region of interest with GridBuilder and Google Maps
First, select the region of interest in GridBuilder, and generate the ROMS grid while noting down some grid parameters listed below (a guide can be found [here](https://austides.com/wp-content/uploads/GridBuilder-v0.99.pdf)). 

GridBuilder parameters to be noted down during grid creation:
- L (xi), M (eta)
- N (levels), Vtransform, theta_s, theta_m, tcline

Next, using Google Maps, mark out a rectangular region that completely encompasses the ROMS grid, and note down the latitudes and longitudes of the corners. 

![HYCOM region selection](https://github.com/yifanye2015/pyroms/blob/main/region_selection_with_hycom.png)

### Creating a new project
This is an overview of the pyroms directory structure:
```
pyroms/
├── setup_conda_env_py38.bash
├── setup_conda_env_opendap_py313.bash
├── environment_py38.yaml
├── environment_opendap_py313.yaml
├── start_new_project.bash
├── template_project/
│   ├── hycom_processing/
│   │   └── scripts.py
│   ├── merra2_opendap_processing/
│   │   └── scripts.py
│   ├── merra2_processing/ (*legacy)
│   │   └── scripts.py
│   ├── output_files/
│   │   └── files.nc
│   ├── .env(.template)
│   ├── config.env
│   ├── run_pyroms_hycom.bash
│   ├── run_pyroms_merra2_opendap.bash
│   └── run_pyroms_merra2.bash
├── examples/
├── pyroms/
├── pyroms_toolbox/
└── bathy_smoother/
```

There is a template directory `template_project` in the top pyroms directory, which contains subdirectories `hycom_processing`, `merra2_opendap_processing`, `merra2_processing` and `output_files`. `hycom_processing` contains scripts that process HYCOM files to produce boundary, climate, and initial condition files, and `merra2_processing`/`merra2_opendap_processing` contains scripts that process MERRA-2 files to produce forcing files. Processed files can be found in `output_files`.

All necessary scripts and subdirectories are in the template directory and should not be changed. Ideally the only things needed to be run/edited/opened are:
- `setup_conda_env_py38.bash` and `setup_conda_env_opendap_py313.bash` for initial conda setup
- `start_new_project.bash` to create a new project directory
- `.env` for storing login credentials (when a new project is created, `.env.template` will be replaced with `.env` automatically)
- `config.env` for setting project parameters
- `run_pyroms_hycom.bash` and either `run_pyroms_merra2.bash` or `run_pyroms_merra2_opendap.bash` to run the processing scripts
- `output_files` for retrieving processed files

To create a new project, simply run:
```
./start_new_project.sh
```
where you will be prompted for a project name, and the project directory will be created.

From here on, activate the appropriate conda environment before running any scripts (*might include code to check this at runtime*).
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

Change your conda environment to the `pyroms-py38` environment using `conda activate pyroms-py38` if it is not yet activated.

For the first run, or if **any** GridBuilder grid parameters/filename/location have been changed in `config.env`, include a `-g` flag to update `gridid.txt`:
```
./run_pyroms_hycom.bash -g
```
For other runs, the `-g` flag may be omitted:
```
./run_pyroms_hycom.bash
```

Python scripts can also be run individually with generated files remaining in `hycom_processing`; ensure `source config.env` is run before that.

Boundary, climate, and initial condition files are successfully generated in `output_files`.

### MERRA-2 data
There are two scripts available. The `merra2_opendap` script is generally much faster but requires a higher Python version incompatible with the HYCOM scripts. 

#### Using merra2_opendap (recommended)
First, go to [NASA Earthdata](https://urs.earthdata.nasa.gov) to create an account, and store your username and password in `~/.netrc` with the following format (change `username` and `password!@#$` only, without quotes):

```
machine urs.earthdata.nasa.gov
    login username
    password password!@#$
```

Run `chmod 600 ~/.netrc` to update the permissions of `.netrc`.

In `config.env`, change/update these variables (do not use spaces):
- MERRA2_START_DATE, MERRA2_END_DATE (date range to analyse)

Save the file.

Change your conda environment to the `pyroms-opendap-py313` environment using `conda activate pyroms-opendap-py313` if it is not yet activated.

Run all scripts with
```
./run_pyroms_merra2_opendap.bash
```

Python scripts can also be run individually with generated files remaining in `merra2_opendap_processing`; ensure `source config.env` is run before that, and run `./add_coordinates_attribute.bash` followed by `join_daily_records.py` after running the scripts.

Forcing files are successfully generated in `output_files`.

#### Using merra2 (legacy)
First, go to [NASA Earthdata](https://urs.earthdata.nasa.gov) to create an account, and store your username and password in `.env`. 

In `config.env`, change/update these variables (do not use spaces):
- MERRA2_START_DATE, MERRA2_END_DATE (date range to analyse)

Save the file.

Change your conda environment to the `pyroms-py38` environment using `conda activate pyroms-py38` if it is not yet activated.

Run all scripts with
```
./run_pyroms_merra2.bash
```

Python scripts can also be run individually with generated files remaining in `merra2_processing`; ensure `source config.env` is run before that, and run `./add_coordinates_attribute.bash` after running the scripts.

Forcing files are successfully generated in `output_files`.
