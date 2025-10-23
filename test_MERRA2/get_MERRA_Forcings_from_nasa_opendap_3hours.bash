#!/bin/bash
set -e

echo -n "Enter a year to process: ";read year; echo ""

start_time=$(date +%s)

source config.env

echo "============================="
echo " Starting MERRA2 processing for year $year "
echo " Started at: $(date)"
echo "============================="
echo ""

echo "Starting Tair..."
python3 get_MERRA_Tair_from_nasa_opendap_3hours.py $year
echo "1/11 Tair done"
echo "----------------------"

echo "Starting Pair..."
python3 get_MERRA_Pair_from_nasa_opendap_3hours.py $year
echo "2/11 Pair done"
echo "----------------------"

echo "Starting Qair..."
python3 get_MERRA_Qair_from_nasa_opendap_3hours.py $year
echo "3/11 Qair done"
echo "----------------------"

echo "Starting Uwind..."
python3 get_MERRA_Uwind_from_nasa_opendap_3hours.py $year
echo "4/11 Uwind done"
echo "----------------------"

echo "Starting Vwind..."
python3 get_MERRA_Vwind_from_nasa_opendap_3hours.py $year
echo "5/11 Vwind done"
echo "----------------------"

echo "Starting lwrad..."
python3 get_MERRA_lwrad_down_from_nasa_opendap_3hours.py $year
echo "6/11 lwrad done"
echo "----------------------"

echo "Starting swrad..."
python3 get_MERRA_swrad_from_nasa_opendap_3hours.py $year
echo "7/11 swrad done"
echo "----------------------"

echo "Starting rain..."
python3 get_MERRA_rain_from_nasa_opendap_3hours.py $year
echo "8/11 rain done"echo "----------------------"

echo "Starting snow..."
python3 get_MERRA_snow_from_nasa_opendap_3hours.py $year
echo "9/11 snow done"
echo "----------------------"

echo "Starting cloud..."
python3 get_MERRA_cloud_from_nasa_opendap_3hours.py $year
echo "10/11 cloud done"
echo "----------------------"

echo "Starting albedo..."
python3 get_MERRA_albedo_from_nasa_opendap_daily.py $year
echo "11/11 albedo done"
echo "----------------------"

echo "Adding coordinate attributes..."
./add_coordinates_attribute.bash
echo "Added coordinate attributes."

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