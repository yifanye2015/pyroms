import matplotlib
matplotlib.use('Agg')

import numpy as np
import netCDF4
from datetime import datetime
import pyroms
import pyroms_toolbox
import sys
import os
import pandas as pd

lon_index_lower = 1253
lon_index_upper = 1300
lat_index_lower = 2136
lat_index_upper = 2140

def create_HYCOM_file(name, time, lon, lat, z, var):

    print('Writing to %s' %name)

    #create netCDF file
    nc = netCDF4.Dataset(name, 'w', format='NETCDF3_64BIT')
    nc.Author = sys._getframe().f_code.co_name
    nc.Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nc.title = 'HYCOM + NCODA Global 1/12 Analysis (GLBy0.08)'

    #create dimensions
    Mp, Lp = lon.shape
    N = len(z)
    nc.createDimension('lon', Lp)
    nc.createDimension('lat', Mp)
    nc.createDimension('z', N)
    nc.createDimension('ocean_time', None)

    #create variables        
    nc.createVariable('lon', 'f', ('lat', 'lon'))
    nc.variables['lon'].long_name = 'longitude'
    nc.variables['lon'].units = 'degrees_east'
    nc.variables['lon'][:] = lon

    nc.createVariable('lat', 'f', ('lat', 'lon'))
    nc.variables['lat'].long_name = 'latitude'
    nc.variables['lat'].units = 'degrees_north'
    nc.variables['lat'][:] = lat

    nc.createVariable('z', 'f', ('z'))
    nc.variables['z'].long_name = 'depth'
    nc.variables['z'].units = 'meter'
    nc.variables['z'][:] = z

    nc.createVariable('ocean_time', 'f', ('ocean_time'))
    nc.variables['ocean_time'].units = 'days since 1900-01-01 00:00:00'
    nc.variables['ocean_time'].calendar = 'LEAP'
    nc.variables['ocean_time'][0] = time

    nc.createVariable(outvarname, 'f', ('ocean_time', 'z', 'lat', 'lon'), fill_value=spval)
    nc.variables[outvarname].long_name = long_name
    nc.variables[outvarname].units = units
    nc.variables[outvarname].coordinates = 'lon lat'
    nc.variables[outvarname][0] = var

    nc.close()

    print('Done with file %s' %name)




# get HYCOM Northeast Pacific data from 2007 to 2011

year = int(os.getenv("YEAR"))
year_tag = '%04d' %year

invarname = 'water_temp'
outvarname = 'temp'

#read grid and variable attributes from the first file
url='http://tds.hycom.org/thredds/dodsC/datasets/GLBy0.08/expt_93.0/data/hindcasts/'+ str(year) + '/hycom_glby_930_' + str(year) + '010112_t000_ts3z.nc'
dataset = netCDF4.Dataset(url)

lon = dataset.variables['lon'][lon_index_lower:lon_index_upper] # without +-1
lat = dataset.variables['lat'][lat_index_lower:lat_index_upper] # without +-1

lon, lat = np.meshgrid(lon, lat)
lon = np.asarray(lon)
lat = np.asarray(lat)

z = dataset.variables['depth'][:]
#spval = dataset.variables[invarname]._FillValue
units = dataset.variables[invarname].units
long_name = dataset.variables[invarname].long_name
dataset.close()


retry_day = []


start_date = os.getenv("HYCOM_START_DATE")
end_date = os.getenv("HYCOM_END_DATE")

# Create proper datetime objects
start_datetime = pd.to_datetime(f"{year_tag}{start_date}", format="%Y%m%d")
end_datetime = pd.to_datetime(f"{year_tag}{end_date}", format="%Y%m%d")

# Generate all dates from start to end (inclusive)
date_range = pd.date_range(start_datetime, end_datetime, freq="D")

# Format back to MMDD (zero-padded)
date_list = [d.strftime("%m%d") for d in date_range]
n_days = len(date_list) # Number of days to process

print(f"Dates to process in year {year} (mmdd):")
print(date_list)
print("----------------------")


for date_tag in date_list:
    print('Processing file for %s, day %02d, month %02d, year %04d' %(invarname,int(date_tag[-2:]),int(date_tag[:2]),int(year_tag)))
    url='http://tds.hycom.org/thredds/dodsC/datasets/GLBy0.08/expt_93.0/data/hindcasts/'+ year_tag +'/hycom_glby_930_' + year_tag + date_tag + '12_t000_ts3z.nc' # Changed URL according to previous url
    #get data from server
    try:
        dataset = netCDF4.Dataset(url)
        var = dataset.variables[invarname][0,:,lat_index_lower:lat_index_upper,lon_index_lower:lon_index_upper] # lat,lon
        #Range are set obtain from MATLAB
        spval = var.get_fill_value()
        dataset.close()
        print('Got %s from server...' %invarname)
    except:
        print('No file on the server... We skip this day.')
        retry_day.append(f"{year_tag}{date_tag}")
        continue

    #create netCDF file
    period = pd.Period(pd.to_datetime(f"{year_tag}{date_tag}", format="%Y%m%d"), freq='H') #Using panda library to convert date format
    day = period.dayofyear #Convert to Julian day
    outfile = 'data/HYCOM_GLBy0.08_%s_%04d_%03d.nc' %(outvarname,year,day)
    jday = pyroms_toolbox.date2jday(datetime(year, 1, 1)) + day - 1
    create_HYCOM_file(outfile, jday, lon, lat, z, var)

print("----------------------")
if len(retry_day) == 0:
    print(f'Temperature files from {year_tag}{start_date} to {year_tag}{end_date} ({n_days} {"day" if n_days == 1 else "days"}) downloaded successfully.')
else:
    print('No files on these days:')
    print(retry_day)
