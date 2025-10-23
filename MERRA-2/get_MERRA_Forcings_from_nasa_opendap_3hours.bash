#!/bin/bash

echo -n "Enter a year to process: ";read year; echo ""


python3 get_MERRA_Tair_from_nasa_opendap_3hours.py $year
echo " 1/11 Tair done"
python3 get_MERRA_Pair_from_nasa_opendap_3hours.py $year
echo " 2/11 Pair done"
python3 get_MERRA_Qair_from_nasa_opendap_3hours.py $year
echo " 3/11 Qair done"
python3 get_MERRA_Uwind_from_nasa_opendap_3hours.py $year
echo " 4/11 Uwind done"
python3 get_MERRA_Vwind_from_nasa_opendap_3hours.py $year
echo " 5/11 Vwind done"
python3 get_MERRA_lwrad_down_from_nasa_opendap_3hours.py $year
echo " 6/11 lwrad done"
python3 get_MERRA_swrad_from_nasa_opendap_3hours.py $year
echo " 7/11 swrad done"
python3 get_MERRA_rain_from_nasa_opendap_3hours.py $year
echo " 8/11 rain done"
python3 get_MERRA_snow_from_nasa_opendap_3hours.py $year
echo " 9/11 snow done"
python3 get_MERRA_cloud_from_nasa_opendap_3hours.py $year
echo "10/11 cloud done"
python3 get_MERRA_albedo_from_nasa_opendap_daily.py $year
echo "11/11 albedo done"
