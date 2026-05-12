#!/bin/bash
set -e

# Change to the directory containing this script
script_dir=$(cd "$(dirname "$0")" && pwd)
cd "$script_dir"

source config.env

cd "$script_dir/merra2_opendap_processing"

year=${YEAR}

start_time=$(date +%s)

echo "============================="
echo " Starting MERRA2 processing for year $year "
echo " Started at: $(date)"
echo "============================="
echo ""

echo "Starting SLV (Pair, Qair, Tair, Uwind, Vwind)..."
python3 get_MERRA_slv.py
echo "5/11 Pair, Qair, Tair, Uwind, Vwind done"
echo "----------------------"

echo "Starting RAD (swrad, lwrad_down, cloud, albedo)..."
python3 get_MERRA_rad.py
echo "9/11 swrad, lwrad_down, cloud, albedo done"
echo "----------------------"

echo "Starting INT (rain, snow)..."
python3 get_MERRA_int.py
echo "11/11 rain, snow done"
echo "----------------------"

echo "Adding coordinate attributes..."
./add_coordinates_attribute.bash
echo "Added coordinate attributes."

echo "Joining daily records into monthly files..."
python3 join_daily_records.py

echo "MERRA-2 monthly forcing files created in output_files/merra2_opendap_files/Forcings"

end_time=$(date +%s)
elapsed=$(( end_time - start_time ))

# Format runtime in hours:minutes:seconds
hours=$(( elapsed / 3600 ))
minutes=$(( (elapsed % 3600) / 60 ))
seconds=$(( elapsed % 60 ))

echo "============================="
echo " All MERRA2 forcing files for $year completed successfully."
echo " Finished at: $(date)"
printf " Total runtime: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
echo "============================="