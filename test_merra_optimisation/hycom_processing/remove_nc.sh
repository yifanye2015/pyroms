#!/bin/bash

# This script just removes all the generated .nc files from hycom scripts
script_dir=$(cd "$(dirname "$0")" && pwd)
cd "$script_dir"
rm remap*.nc data/*.nc data/raw/*.nc bdry/*.nc clm/*.nc ic/*.nc