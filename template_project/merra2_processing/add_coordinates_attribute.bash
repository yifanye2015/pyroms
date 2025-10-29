lst=`ls Forcings/MERRA2_Pair_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,Pair,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_Qair_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,Qair,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_Tair_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,Tair,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_Uwind_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,Uwind,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_Vwind_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,Vwind,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_cloud_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,cloud,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_lwrad_down_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,lwrad_down,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_rain_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,rain,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_snow_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,snow,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_swrad_3hours_*`
for file in $lst ; do
ncatted -O -a coordinates,swrad,o,c,'lon lat' $file
done

lst=`ls Forcings/MERRA2_albedo_daily_*`
for file in $lst ; do
ncatted -O -a coordinates,albedo,o,c,'lon lat' $file
done

