#!/bin/bash
# =========================================================
# install_scrip.sh
# Installs SCRIP library for pyroms
# =========================================================

set -e  # Stop on error

# Change to the directory containing this script
script_dir=$(cd "$(dirname "$0")" && pwd)
cd "$script_dir"

echo "Installing pyroms components in editable mode..."
cd ..
pip install -e pyroms/pyroms
pip install -e pyroms/pyroms_toolbox
pip install -e pyroms/bathy_smoother

echo "Building SCRIP..."
cd pyroms/pyroms/external/scrip/source/

# Automatically detect conda env prefix
PREFIX=$(python -c "import sys; print(sys.prefix)")
echo "Using PREFIX = $PREFIX"

make DEVELOP=1 PREFIX=$PREFIX install

echo "Moving built SCRIP library into pyroms..."
mv -vf scrip*.so ../../../pyroms/

echo "Installation complete."
