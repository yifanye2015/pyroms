import matplotlib
matplotlib.use('Agg')

import numpy as np
import netCDF4
from datetime import datetime
import pyroms
import pyroms_toolbox
import sys
import pandas as pd


def create_HYCOM_file(name, time, lon, lat, z, var):

    print('Write with file %s' %name)

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

year = 2019
retry='False'

invarname = 'water_temp'
outvarname = 'temp'

year_tag = '%04d' %year

#read grid and variable attributes from the first file
url='http://tds.hycom.org/thredds/dodsC/datasets/GLBy0.08/expt_93.0/data/hindcasts/2019/hycom_glby_930_2019010112_t000_ts3z.nc'
#url='http://tds.hycom.org/thredds/dodsC/datasets/GLBa0.08/expt_91.1/2015/temp/archv.2015_001_00_3zt.nc'
dataset = netCDF4.Dataset(url)

lon = dataset.variables['lon'][1253:1300] # without +-1
lat = dataset.variables['lat'][2136:2140] # without +-1

lon, lat = np.meshgrid(lon, lat)
lon = np.asarray(lon)
lat = np.asarray(lat)

z = dataset.variables['depth'][:]
#spval = dataset.variables[invarname]._FillValue
units = dataset.variables[invarname].units
long_name = dataset.variables[invarname].long_name
dataset.close()


retry_day = []

###############
# loop over daily files
if year%4 == 0:
    # daysinyear = 366
    daysinmonth = ([0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
else:
    # daysinyear = 365
    daysinmonth = ([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

# range(x,y+1) means to download data from start of month x to end of month y, so (5,6+1) means from 1 may to 30 jun
for month in range(5,5+1):
    month_tag = '%02d' %(month)
    for day in range(1,1+1): # range excludes upper bound, if using all days of the month then use range(1,daysinmonth[month]+1)
        day_tag = '%02d' %(day)
        date_tag = year_tag + month_tag + day_tag
        print('Processing file for %s, day %02d, month %02d, year %04d' %(invarname,day,month,year))
        url='http://tds.hycom.org/thredds/dodsC/datasets/GLBy0.08/expt_93.0/data/hindcasts/'+ year_tag +'/hycom_glby_930_' + date_tag + '12_t000_ts3z.nc' # Changed URL according to previous url
        #get data from server
        try:
            dataset = netCDF4.Dataset(url)
            var = dataset.variables[invarname][0,:,2136:2140,1253:1300] # lat,lon
            #Range are set obtain from MATLAB
            spval = var.get_fill_value()
            dataset.close()
            print('Got %s from server...' %invarname)
        except:
            print('No file on the server... We skip this day.')
            retry_day.append(day)
            continue

    #create netCDF file
    date_dash = year_tag + '-' + month_tag + '-' + day_tag
    period = pd.Period(date_dash, freq='H') #Using panda library to convert date format
    day = period.dayofyear #Convert to Julian day
    outfile = 'data/HYCOM_GLBy0.08_%s_%04d_%03d.nc' %(outvarname,year,day)
    jday = pyroms_toolbox.date2jday(datetime(year, 1, 1)) + day - 1
    create_HYCOM_file(outfile, jday, lon, lat, z, var)

###############

# # loop over daily files
# if year%4 == 0:
#     daysinyear = 366
# else:
# #    daysinyear = 365
#     daysinyear = 32
# for day in range(1,daysinyear+1):
#     print('Processing file for %s, day %03d, year %04d' %(invarname, day, year))
#     url='http://tds.hycom.org/thredds/dodsC/datasets/GLBa0.08/expt_91.1/2015/temp/archv.%04d_%03d_00_3zt.nc' %(year,day)
#     #get data from server
#     try:
#         dataset = netCDF4.Dataset(url)
#         var = dataset.variables[invarname][0,:,1500-9:1800,600:940]
#         spval = var.get_fill_value()
#         dataset.close()
#         print('Got %s from server...' %invarname)
#     except:
#         print('No file on the server... We skip this day.')
#         retry_day.append(day)
#         continue

#     #create netCDF file
#     outfile = 'data/HYCOM_GLBa0.08_%s_%04d_%03d.nc' %(outvarname,year,day)
#     jday = pyroms_toolbox.date2jday(datetime(year, 1, 1)) + day - 1
#     create_HYCOM_file(outfile, jday, lon, lat, z, var)


# if retry == 'True':
#     if len(retry_day) != 0:
#         print("Some file have not been downloded... Let's try again")
#     while len(retry_day) != 0:
#         for day in retry_day:
#             print('Retry file for %s, day %03d, year %04d' %(invarname, day, year))
#             url='http://tds.hycom.org/thredds/dodsC/datasets/GLBa0.08/expt_91.1/2015/temp/archv.%04d_%03d_00_3zt.nc' %(year,day)
#             #get data from server
#             try:
#                 dataset = netCDF4.Dataset(url)
#                 var = dataset.variables[invarname][0,:,1500-9:1800,600:940]
#                 spval = var.get_fill_value()
#                 dataset.close()
#                 print('Got %s from server...' %invarname)
           
#             except:
#                 print('No file on the server... We skip this day.')
#                 continue

#             #create netCDF file
#             outfile = 'data/HYCOM_GLBa0.08_%s_%04d_%03d.nc' %(outvarname,year,day)
#             jday = pyroms_toolbox.date2jday(datetime(year, 1, 1)) + day - 1
#             create_HYCOM_file(outfile, jday, lon, lat, z, var)

#             retry_day.remove(day)


