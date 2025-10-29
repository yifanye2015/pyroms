import subprocess
import os
import sys
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use('Agg')

import pyroms
import pyroms_toolbox

from remap_clm import remap_clm
from remap_clm_uv import remap_clm_uv

lst_year = sys.argv[1:]

project_name = os.getenv("PROJECT_NAME")
grid_id = project_name.upper()

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data/')
dst_dir = os.path.join(script_dir, 'clm/')

lst_file = []

for year in lst_year:
    year = str(year)
    # lst = commands.getoutput('ls ' + data_dir + '*' + year + '*')
    # lst = commands.getoutput('ls ' + data_dir + 'SODA_2.1.6_' + year + '_0*')
    lst = subprocess.getoutput('ls ' + data_dir + 'HYCOM_GLBy0.08_merged_' + year + '*')
    lst = lst.split()
    lst_file = lst_file + lst

print('Build CLM file from the following file list:')
print(lst_file)
print(' ')

src_grd_file = os.path.join(data_dir, 'HYCOM_GLBy0.08_' + project_name + '_grid.nc')
src_grd = pyroms_toolbox.Grid_HYCOM.get_nc_Grid_HYCOM(src_grd_file)
dst_grd = pyroms.grid.get_ROMS_grid(grid_id)


for file in lst_file:
# remap
    zeta = remap_clm(file, 'ssh', src_grd, dst_grd, dst_dir=dst_dir)
    dst_grd = pyroms.grid.get_ROMS_grid(grid_id, zeta=zeta)
    remap_clm(file, 'temp', src_grd, dst_grd, dst_dir=dst_dir)
    remap_clm(file, 'salt', src_grd, dst_grd, dst_dir=dst_dir)
    remap_clm_uv(file, src_grd, dst_grd, dst_dir=dst_dir)

# merge file
    clim_file = dst_dir + file.rsplit('/')[-1][:-3] + '_clim_' + dst_grd.name + '.nc'

    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_ssh_clim_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-O', out_file, clim_file)
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_temp_clim_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-A', out_file, clim_file)
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_salt_clim_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-A', out_file, clim_file)
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_u_clim_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-A', out_file, clim_file)
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_v_clim_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-A', out_file, clim_file)
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
