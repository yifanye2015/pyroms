import subprocess
import os
import subprocess
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')

import pyroms
import pyroms_toolbox

from remap import remap
from remap_uv import remap_uv

project_name = os.getenv("PROJECT_NAME")
grid_id = project_name.upper()

# keep either A or B, comment out the other
# if using A, use C; if using B, use D

# A - for a specific data file; no need to enter year
#####
# file = '/home/yeyifan/pyroms/Palau_HYCOM/data/HYCOM_GLBy0.08_2019_121.nc'
# data_dir = './data/'
# dst_dir='./ic/'

# print('Build IC file from the following file:')
# print(file)
# print(' ')
#####

# B - for a whole year; need to enter year as argument when running the .py file
#####
lst_year = sys.argv[1:]

data_dir = './data/'
dst_dir='./ic/'

lst_file = []

for year in lst_year:
    year = str(year)
    command = 'ls ' + data_dir + 'HYCOM_GLBy0.08_merged_' + year + '*'
    lst = subprocess.check_output(command, shell=True).decode().split()
    lst_file.extend(lst)

print('Build IC file from the following files:')
print(lst_file)
print(' ')
#####

src_grd_file = data_dir + 'HYCOM_GLBy0.08_' + project_name + '_grid.nc'
src_grd = pyroms_toolbox.Grid_HYCOM.get_nc_Grid_HYCOM(src_grd_file)
dst_grd = pyroms.grid.get_ROMS_grid(grid_id)

# C - use with A
#####
# # remap
# zeta = remap(file, 'ssh', src_grd, dst_grd, dst_dir=dst_dir)
# dst_grd = pyroms.grid.get_ROMS_grid('PENANG', zeta=zeta)
# remap(file, 'temp', src_grd, dst_grd, dst_dir=dst_dir)
# remap(file, 'salt', src_grd, dst_grd, dst_dir=dst_dir)
# remap_uv(file, src_grd, dst_grd, dst_dir=dst_dir)

# # merge file
# ic_file = dst_dir + file.rsplit('/')[-1][:-3] + '_ic_' + dst_grd.name + '.nc'

# out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_ssh_ic_' + dst_grd.name + '.nc'
# command = ('ncks', '--no-alphabetize', '-O', out_file, ic_file) 
# #print(command)
# subprocess.check_call(command)
# os.remove(out_file)
# out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_temp_ic_' + dst_grd.name + '.nc'
# command = ('ncks', '--no-alphabetize', '-A', out_file, ic_file) 
# #print(command)
# subprocess.check_call(command)
# os.remove(out_file)
# out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_salt_ic_' + dst_grd.name + '.nc'
# command = ('ncks', '--no-alphabetize', '-A', out_file, ic_file) 
# #print(command)
# subprocess.check_call(command)
# os.remove(out_file)
# out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_u_ic_' + dst_grd.name + '.nc'
# command = ('ncks', '--no-alphabetize', '-A', out_file, ic_file) 
# #print(command)
# subprocess.check_call(command)
# os.remove(out_file)
# out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_v_ic_' + dst_grd.name + '.nc'
# command = ('ncks', '--no-alphabetize', '-A', out_file, ic_file) 
# #print(command)
# subprocess.check_call(command)
# os.remove(out_file)
#####

# D - use with B
#####
for file in lst_file:
# remap
    zeta = remap(file, 'ssh', src_grd, dst_grd, dst_dir=dst_dir)
    dst_grd = pyroms.grid.get_ROMS_grid(grid_id, zeta=zeta)
    remap(file, 'temp', src_grd, dst_grd, dst_dir=dst_dir)
    remap(file, 'salt', src_grd, dst_grd, dst_dir=dst_dir)
    remap_uv(file, src_grd, dst_grd, dst_dir=dst_dir)

# merge file
    ic_file = dst_dir + file.rsplit('/')[-1][:-3] + '_ic_' + dst_grd.name + '.nc'

    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_ssh_ic_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-O', out_file, ic_file) 
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_temp_ic_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-A', out_file, ic_file) 
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_salt_ic_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-A', out_file, ic_file) 
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_u_ic_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-A', out_file, ic_file) 
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
    out_file = dst_dir + file.rsplit('/')[-1][:-3] + '_v_ic_' + dst_grd.name + '.nc'
    command = ('ncks', '--no-alphabetize', '-A', out_file, ic_file) 
    #print(command)
    subprocess.check_call(command)
    os.remove(out_file)
#####