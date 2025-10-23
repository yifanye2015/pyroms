import matplotlib
matplotlib.use('Agg')
import pyroms
import pyroms_toolbox

# load the grid
srcgrd = pyroms_toolbox.Grid_HYCOM.get_nc_Grid_HYCOM('/home/yeyifan/pyroms/Palau_HYCOM/HYCOM_GLBy0.08_penang_grid.nc')
dstgrd = pyroms.grid.get_ROMS_grid('PENANG') # all CAPS

# make remap grid file for scrip
pyroms_toolbox.Grid_HYCOM.make_remap_grid_file(srcgrd)
pyroms.remapping.make_remap_grid_file(dstgrd, Cpos='rho')
pyroms.remapping.make_remap_grid_file(dstgrd, Cpos='u')
pyroms.remapping.make_remap_grid_file(dstgrd, Cpos='v')

# compute remap weights
# input namelist variables for bilinear remapping at rho points
grid1_file = 'remap_grid_GLBy0.08_NEP_t.nc'
grid2_file = 'remap_grid_PENANG_rho.nc'
interp_file1 = 'remap_weights_GLBy0.08_to_PENANG_bilinear_t_to_rho.nc'
interp_file2 = 'remap_weights_PENANG_to_GLBy0.08_bilinear_rho_to_t.nc'
map1_name = 'GLBy0.08 to PENANG Bilinear Mapping'
map2_name = 'PENANG to GLBy0.08 Bilinear Mapping'
num_maps = 1
map_method = 'bilinear'

pyroms.remapping.compute_remap_weights(grid1_file, grid2_file, \
              interp_file1, interp_file2, map1_name, \
              map2_name, num_maps, map_method)


# compute remap weights
# input namelist variables for bilinear remapping at rho points
grid1_file = 'remap_grid_GLBy0.08_NEP_t.nc'
grid2_file = 'remap_grid_PENANG_u.nc'
interp_file1 = 'remap_weights_GLBy0.08_to_PENANG_bilinear_t_to_u.nc'
interp_file2 = 'remap_weights_PENANG_to_GLBy0.08_bilinear_u_to_t.nc'
map1_name = 'GLBy0.08 to PENANG Bilinear Mapping'
map2_name = 'PENANG to GLBy0.08 Bilinear Mapping'
num_maps = 1
map_method = 'bilinear'

pyroms.remapping.compute_remap_weights(grid1_file, grid2_file, \
              interp_file1, interp_file2, map1_name, \
              map2_name, num_maps, map_method)


# compute remap weights
# input namelist variables for bilinear remapping at rho points
grid1_file = 'remap_grid_GLBy0.08_NEP_t.nc'
grid2_file = 'remap_grid_PENANG_v.nc'
interp_file1 = 'remap_weights_GLBy0.08_to_PENANG_bilinear_t_to_v.nc'
interp_file2 = 'remap_weights_PENANG_to_GLBy0.08_bilinear_v_to_t.nc'
map1_name = 'GLBy0.08 to PENANG Bilinear Mapping'
map2_name = 'PENANG to GLBy0.08 Bilinear Mapping'
num_maps = 1
map_method = 'bilinear'

pyroms.remapping.compute_remap_weights(grid1_file, grid2_file, \
              interp_file1, interp_file2, map1_name, \
              map2_name, num_maps, map_method)

