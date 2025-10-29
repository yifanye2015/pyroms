#!/bin/bash

# Change to the directory containing this script
script_dir=$(cd "$(dirname "$0")" && pwd)
cd "$script_dir"

source config.env

cd "$script_dir/hycom_processing"

year=${YEAR}

set -e

start_time=$(date +%s)

echo "============================="
echo " Starting HYCOM processing for year $year "
echo " Started at: $(date)"
echo "============================="
echo ""

# python3 update_gridid.py
python3 get_hycom_GLBy0.08_Palau_grid.py
echo "----------------------"
echo "Starting salt..."
python3 get_hycom_GLBy0.08_salt_2015.py
echo "----------------------"
echo "Starting ssh..."
python3 get_hycom_GLBy0.08_ssh_2015.py
echo "----------------------"
echo "Starting temp..."
python3 get_hycom_GLBy0.08_temp_2015.py
echo "----------------------"
echo "Starting u..."
python3 get_hycom_GLBy0.08_u_2015.py
echo "----------------------"
echo "Starting v..."
python3 get_hycom_GLBy0.08_v_2015.py
echo "----------------------"
cd data/
ksh merge_HYCOM_GLBy0.08_daily.ksh
echo "----------------------"
cd ../
python3 make_remap_weights_file.py
echo "Remap weights done."
echo "----------------------"
python3 make_bdry_file.py ${YEAR}
echo "Boundary file done."
echo "----------------------"
python3 make_clm_file.py ${YEAR}
echo "Climate file done."
echo "----------------------"
python3 make_ic_file.py ${YEAR}
echo "IC file done."
echo "----------------------"

echo "All scripts run successfully."

cp bdry/*.nc ../output_files/hycom_files/bdry/
cp clm/*.nc ../output_files/hycom_files/clm/
cp ic/*.nc ../output_files/hycom_files/ic/

echo "HYCOM boundary, climate, IC files copied to output_files/hycom_files"

end_time=$(date +%s)
elapsed=$(( end_time - start_time ))

# Format runtime in hours:minutes:seconds
hours=$(( elapsed / 3600 ))
minutes=$(( (elapsed % 3600) / 60 ))
seconds=$(( elapsed % 60 ))

echo "============================="
echo " All HYCOM files for $year downloaded and remapped successfully."
echo " Finished at: $(date)"
printf " Total runtime: %02d:%02d:%02d (hh:mm:ss)\n" $hours $minutes $seconds
echo "============================="