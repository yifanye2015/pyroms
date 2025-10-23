import matplotlib
matplotlib.use('Agg')

import numpy as np
import netCDF4
from datetime import datetime
import pyroms
import pyroms_toolbox
import sys
import os

print("Processing HYCOM grid for project " + os.getenv("PROJECT_NAME"))

lon_index_lower = 1253
lon_index_upper = 1300
lat_index_lower = 2136
lat_index_upper = 2140

# get HYCOM Northeast Pacific data from 2007 to 2011

year = int(os.getenv('YEAR'))
day = 1

invarname = 'water_temp'
outvarname = 'temp'

#read grid and variable attributes from the first file
url='http://tds.hycom.org/thredds/dodsC/datasets/GLBy0.08/expt_93.0/data/hindcasts/'+ str(year) + '/hycom_glby_930_' + str(year) + '010112_t000_ts3z.nc'
dataset = netCDF4.Dataset(url)


lon = dataset.variables['lon'][lon_index_lower-1:lon_index_upper+1] #+-1 not a mistake
lat = dataset.variables['lat'][lat_index_lower-1:lat_index_upper+1] #+-1 not a mistake

lon, lat = np.meshgrid(lon, lat)
lon = np.asarray(lon)
lat = np.asarray(lat)

z = dataset.variables['depth'][:]

#spval = dataset.variables[invarname]._FillValue
var = dataset.variables[invarname][0,:,lat_index_lower-1:lat_index_upper+1,lon_index_lower-1:lon_index_upper+1]
spval = var.get_fill_value()
units = dataset.variables[invarname].units
long_name = dataset.variables[invarname].long_name
dataset.close()


#create netCDF file
outfile = 'data/HYCOM_GLBy0.08_' + os.getenv("PROJECT_NAME") + '_grid.nc'
nc = netCDF4.Dataset(outfile, 'w', format='NETCDF3_64BIT')
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
jday = pyroms_toolbox.date2jday(datetime(year, 1, 1)) + day - 1
nc.variables['ocean_time'][0] = jday

nc.createVariable(outvarname, 'f', ('ocean_time', 'z', 'lat', 'lon'), fill_value=spval)
nc.variables[outvarname].long_name = long_name
nc.variables[outvarname].units = units
nc.variables[outvarname][0] = var
        
nc.close()

print('Done with file %s' %outfile)



