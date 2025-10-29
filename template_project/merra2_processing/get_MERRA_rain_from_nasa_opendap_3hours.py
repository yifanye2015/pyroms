import matplotlib
matplotlib.use('Agg')
import numpy as np
import netCDF4
from datetime import datetime
import pyroms
import pyroms_toolbox
import os
import pandas as pd
import sys
from pydap.cas.urs import setup_session
from pydap.client import open_url

server = 'http://goldsmr4.gesdisc.eosdis.nasa.gov'
username = os.getenv("EARTHDATA_USERNAME")
password = os.getenv("EARTHDATA_PASSWORD")

year = int(sys.argv[1])
year_tag = '%04d' %year

invarname1 = 'PRECCU'
invarname2 = 'PRECLS'
invarname3 = 'PRECSN'

outvarname = 'rain'
outtimename = 'rain_time'


#if (year <= 1992):
#    file_tag = 'MERRA101'
#elif ((year >= 1993) & (year <= 2000)):
#    file_tag = 'MERRA201'
#elif ((year >= 2001) & (year <= 2009)):
#    file_tag = 'MERRA301'
#elif (year >= 2010):
#    file_tag = 'MERRA300'
file_tag = 'MERRA2_400'


# Date range processing
start_date = os.getenv("MERRA2_START_DATE")
end_date = os.getenv("MERRA2_END_DATE")

start_month = int(start_date[0:2])
end_month = int(end_date[0:2])
month_range = range(start_month, end_month + 1) # integers not zero-padded

# Create proper datetime objects
start_datetime = pd.to_datetime(f"{year_tag}{start_date}", format="%Y%m%d")
end_datetime = pd.to_datetime(f"{year_tag}{end_date}", format="%Y%m%d")

# Generate all dates from start to end (inclusive)
date_range = pd.date_range(start_datetime, end_datetime, freq="D")

# Format back to MMDD (zero-padded)
date_list = [d.strftime("%m%d") for d in date_range]
n_days = len(date_list) # Number of days to process

# Group date_list by month (e.g., [[0227,0228],[0301,...,0331],[0401,...]])
date_list_by_month = []
current_month = date_list[0][:2]
month_group = []

for d in date_list:
    month = d[:2]
    if month != current_month:
        date_list_by_month.append(month_group)
        month_group = []
        current_month = month
    month_group.append(d)

# Append the last group
if month_group:
    date_list_by_month.append(month_group)

# Optional: print to verify
# print(date_list_by_month)


print(f'{n_days} {"day" if n_days == 1 else "days"} to process in year {year} (mmdd):')
print(date_list)
print("----------------------")


# Read grid and variable attributes from the first file
month_tag = '01'
day_tag = '01'
date_tag = year_tag + month_tag + day_tag
url = server + '/opendap/MERRA2/M2T1NXINT.5.12.4/' + year_tag + '/' + month_tag + '/' + \
      file_tag + '.tavg1_2d_int_Nx.' + date_tag + '.nc4'

print(f'Processing day 1 MERRA-2 {outvarname} data for year {year_tag}...')

session = setup_session(username,password,url)
dataset = open_url(url, session = session)

lon = dataset['lon'][:]
lon = np.asarray(lon)
#shift data between 0 and 360 deg.
gidx = np.where(np.abs(lon) < 1.0e-10)[0][0]
lon = lon + 180.0
lat = dataset['lat'][:]
lat = np.asarray(lat)
spval = dataset[invarname2].missing_value
units = dataset[invarname2].units
long_name = 'Total Precipitation'


month_range_idx = 0

# Get data from NASA opendap
for month in month_range:
    nday = 0

    #create ROMS forcing file
    month_tag = '%02d' %(month)
    outfile = 'Forcings/MERRA2_' + outvarname + '_3hours_' + year_tag + '_' + month_tag + '.nc'
    nc = netCDF4.Dataset(outfile, 'w', format='NETCDF3_64BIT')
    nc.Author = sys._getframe().f_code.co_name
    nc.Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nc.title = 'MERRA-2 dataset. Modern Era Retrospective-analysis'

    nc.createDimension('lon', np.size(lon))
    nc.createDimension('lat', np.size(lat))
    nc.createDimension(outtimename, None)

    nc.createVariable('lon', 'f8', ('lon'))
    nc.variables['lon'].long_name = 'longitude'
    nc.variables['lon'].units = 'degrees_east'
    nc.variables['lon'][:] = lon

    nc.createVariable('lat', 'f8', ('lat'))
    nc.variables['lat'].long_name = 'latitude'
    nc.variables['lat'].units = 'degrees_north'
    nc.variables['lat'][:] = lat

    nc.createVariable(outtimename, 'f8', (outtimename))
    nc.variables[outtimename].units = 'days since 1900-01-01 00:00:00'
    nc.variables[outtimename].calendar = 'LEAP'
    
    dstart = pyroms_toolbox.date2jday(datetime(year, month, int(date_list_by_month[month_range_idx][0][2:4]), 0, 0)) # year, month, day, hr, min; returns a float
    dstop = pyroms_toolbox.date2jday(datetime(year, month, int(date_list_by_month[month_range_idx][-1][2:4]), 0, 0))
    roms_time = np.arange(dstart, dstop + 1, 3./24) # x./24 means sampling every x hrs; +1 here to include the last day, also avoids errors when crossing a month or year
    nc.variables[outtimename][:] = roms_time

    nc.createVariable(outvarname, 'f', (outtimename, 'lat', 'lon'), fill_value=spval)
    nc.variables[outvarname].long_name = long_name
    nc.variables[outvarname].units = units
    nc.variables[outvarname].coordinates = 'lon lat'

    for day in date_list_by_month[month_range_idx]:
#    if year == 2010:
#      if ((month+1 >= 6) & (month+1 <= 8)):
#        file_tag = 'MERRA301'
#      else:
#        file_tag = 'MERRA300'
        day_tag = day[2:4]
        date_tag = year_tag + month_tag + day_tag
        url = server + '/opendap/MERRA2/M2T1NXINT.5.12.4/' + year_tag + '/' + month_tag + '/' + \
                file_tag + '.tavg1_2d_int_Nx.' + date_tag + '.nc4'
        
        print(f'Processing MERRA-2 {outvarname} data for day {day_tag}, month {month_tag}, year {year_tag}...')

        dataset = open_url(url, session = session)

        var = np.asarray(dataset[invarname1][:]) + np.asarray(dataset[invarname2][:]) + np.asarray(dataset[invarname3][:]) # total precipitation
        var = np.asarray(var)
        #shift data between 0 and 360 deg.
        svar = np.zeros(var.shape)
        svar[:,:,:len(lon)-gidx] = var[:,:,gidx:]
        svar[:,:,len(lon)-gidx:] = var[:,:,:gidx]
        
        var_3hr = (svar[::3] + svar[1::3] + svar[2::3]) / 3.
        nc.variables[outvarname][nday*8:(nday+1)*8,:,:] = var_3hr
        nday = nday + 1
#       dataset.close()

    nc.close()
    month_range_idx = month_range_idx + 1

print("----------------------")
print(f'MERRA-2 {outvarname} files from {year_tag}{start_date} to {year_tag}{end_date} ({n_days} {"day" if n_days == 1 else "days"}) processed successfully.')
