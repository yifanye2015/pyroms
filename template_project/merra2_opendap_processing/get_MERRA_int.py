import matplotlib
matplotlib.use('Agg')
import numpy as np
import netCDF4
import xarray as xr
from datetime import datetime
# import pyroms
# import pyroms_toolbox
import os
import pandas as pd
import sys

import earthaccess
from earthaccess.exceptions import LoginStrategyUnavailable

# import pydap-specific tools
from pydap.client import get_cmr_urls, open_url
from pydap.client import to_netcdf as dap_to_netcdf

# Server: http://goldsmr4.gesdisc.eosdis.nasa.gov

# Dataset information
MERRA2_M2T1NXINT_ccid = "C1276812846-GES_DISC" # short name M2T1NXINT
file_tag = "MERRA2_400.tavg1_2d_int_Nx."

# Date range information
year = int(os.getenv("YEAR"))
start_date = os.getenv("MERRA2_START_DATE")
end_date = os.getenv("MERRA2_END_DATE")

# Date range processing
start_month = int(start_date[0:2])
end_month = int(end_date[0:2])

start_day = int(start_date[2:4])
end_day = int(end_date[2:4])

time_range = [datetime(year, start_month, start_day), datetime(year, end_month, end_day)]

# invarnames, outvarnames, outtimenames must be ordered
invarnames_helper = ['PRECCU', 'PRECLS', 'PRECSN'] # var names in source MERRA2 dataset; helper list to keep code consistent with other scripts
invarnames = ['TOTAL_PREC', 'PRECSN']
outvarnames = ['rain', 'snow']
outtimenames = ['rain_time', 'snow_time']

output_path_int = "./Forcings/INT"
output_path_merra_roms = "./Forcings"


if __name__ == '__main__':
    print(f"Starting download for INT files from {time_range[0]} to {time_range[1]}...")

    # Get urls
    cmr_urls = [urls for urls in get_cmr_urls(ccid=MERRA2_M2T1NXINT_ccid, time_range=time_range, limit=1000)]

    # Login to Earthdata
    try:
        auth = earthaccess.login(strategy="netrc", persist=True) # you will be prompted to add your EDL credentials
    except LoginStrategyUnavailable:
        auth = earthaccess.login(strategy="interactive", persist=True)

    # Pass Token Authorization to a new Session
    my_session = session=auth.get_session()

    # create an Xarray Dataset object. It eagerly downloads all dimension data, which in this case
    # it facilitates our workflow since `latitude` & `longitude` are dimension data.
    ds = xr.open_dataset(cmr_urls[0].replace("https", "dap4"), engine="pydap", session=my_session)

    # Optional for slicing data before downloading
    
    # # Min/max of lon values &  Min/Max of lat values
    # lat_min, lat_max = -90, 90
    # lon_min, lon_max = -180, 180

    # Lon, Lat = ds['lon'], ds['lat']

    # iLon = np.where((Lon>lon_min)&(Lon < lon_max))[0]

    # iLat = np.where((Lat>lat_min)&(Lat < lat_max))[0]

    # ======================================================
    # Create input argument for Streaming a subset of data
    # ======================================================
    dim_slices = {
        # 'lon': (iLon[0], iLon[-1]), 
        # 'lat': (iLat[0], iLat[-1]),
    }

    # Variables from collection
    Variables = [f"/{invarname}" for invarname in invarnames_helper]
    dims = list(set(["/"+dim for var in Variables for dim in ds[var[1:]].dims]))

    # Add dimensions to Variable lists from each collection
    Variables += dims

    dap_to_netcdf(cmr_urls,
                session=my_session,
                keep_variables=Variables,
                dim_slices=dim_slices,
                output_path=output_path_int)
    
    ds.close()

    print(f"Download completed. Starting processing of INT files into ROMS format...")

    # Process each file into ROMS format
    int_filenames = [f for f in os.listdir(output_path_int) if f.startswith(file_tag) and f.endswith(".nc4")]

    for int_filename in int_filenames:
        # Open the INT file
        int_filepath = os.path.join(output_path_int, int_filename)
        ds_int = xr.open_dataset(int_filepath, decode_times=True)
        int_date = int_filename[-12:-4] # extract date from filename, format str(YYYYMMDD)
        time_list_3hourly = pd.date_range(start=int_date, periods=8, freq='3h')

        # Generate total precipitation dataarray first
        ds_int['TOTAL_PREC'] = ds_int['PRECCU'] + ds_int['PRECLS'] + ds_int['PRECSN']

        for varname_idx in range(len(invarnames)):
            invarname = invarnames[varname_idx]
            outvarname = outvarnames[varname_idx]
            outtimename = outtimenames[varname_idx]
            
            ds_var = ds_int[[invarname]].rename({
                invarname: outvarname,
                'time': outtimename
            })



            # 3-hour averaging using explicit indexing and averaging
            outvar_data = ds_var[outvarname]  # Get the DataArray
            var_3hr_data = (outvar_data.isel({outtimename: slice(0, None, 3)}).values + 
                            outvar_data.isel({outtimename: slice(1, None, 3)}).values + 
                            outvar_data.isel({outtimename: slice(2, None, 3)}).values) / 3.0

            # Create a new DataArray with the averaged data and new time coordinate
            var_3hr = xr.DataArray(
                var_3hr_data,
                dims=[outtimename, 'lat', 'lon'],
                coords={
                    outtimename: time_list_3hourly,
                    'lat': ds_var['lat'],
                    'lon': ds_var['lon']
                },
                name=outvarname,
                attrs={
                    'long_name': ds_var[outvarname].long_name if outvarname != 'rain' else 'Total Precipitation',
                    'units': ds_var[outvarname].units if outvarname != 'rain' else ds_int['PRECLS'].units,
                }
            )

            # Convert back to Dataset
            ds_var = var_3hr.to_dataset()

            # lon shift from -180 to 180, to 0 - 360
            ds_var.coords['lon'] = np.mod(ds_var.coords['lon'], 360) # 0 might get shifted to 360, idk how to fix it lol; probably some floating point problem
            ds_var.coords['lon'] = xr.where(np.isclose(ds_var.coords['lon'], 360), 0, ds_var.coords['lon']) # manually set any 360 lon to 0, assumes no lon > 360
            ds_var = ds_var.sortby(ds_var.lon)

            # Update attributes
            ds_var['lat'].attrs.clear()
            ds_var['lat'].attrs['long_name'] = 'latitude'
            ds_var['lat'].attrs['units'] = 'degrees_north'

            ds_var['lon'].attrs['long_name'] = 'longitude'
            ds_var['lon'].attrs['units'] = 'degrees_east'

            ds_var[outtimename].encoding['units'] = 'days since 1900-01-01 00:00:00'
            ds_var[outtimename].encoding['dtype'] = 'float64'

            ds_var.attrs["Author"] = sys._getframe().f_code.co_name
            ds_var.attrs["Created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ds_var.attrs["Title"] = "MERRA-2 dataset. Modern Era Retrospective-analysis"

            # Save file
            outfile = os.path.join(output_path_merra_roms, "MERRA2_" + outvarname + "_3hours_" + int_date[:4] + "_" + int_date[4:] + ".nc")
            ds_var.to_netcdf(outfile, mode="w", unlimited_dims=outtimename) # unlimited_dims for joining files along time dim

        ds_int.close()

    print(f"{', '.join(outvarnames)} 3-hourly files created for {time_range[0]} to {time_range[1]}.")
