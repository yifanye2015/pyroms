import xarray as xr
import numpy as np
import netCDF4
import os

# Path to the grid file
local_grid = os.getenv("GRIDBUILDER_PATH")

# Load the dataset
ds = xr.open_dataset(local_grid).load()
ds.close()

# Extract bathymetry
h = ds['h'].values

# Apply corrections
h_corrected = np.where(h <= 0, 2.0, h)

# Update dataset
ds['h'].values[:] = h_corrected
ds['depthmin'] = h_corrected.min()
ds['depthmax'] = h_corrected.max()

# Save directly back into the same file
ds.to_netcdf(local_grid, mode="w")

print("Bathymetry correction complete.")
# print(f"New depth min: {h_corrected.min()}")
# print(f"New depth max: {h_corrected.max()}")


def index_strictly_lower(array, x):
    """
    Return index i such that lon[i] < x and lon[i] is the largest value < x.
    If no such element exists, return 0.
    """
    x = float(x)
    array = np.asarray(array)
    idx = np.searchsorted(array, x, side='left') - 1
    return max(idx, 0)


def index_strictly_greater(array, x):
    """
    Return index j such that lon[j] > x and lon[j] is the smallest value > x.
    If no such element exists, return len(lon)-1.
    """
    x = float(x)
    array = np.asarray(array)
    idx = np.searchsorted(array, x, side='right')
    return min(idx, len(array)-1)

print("Extracting HYCOM lat/lon index bounds...")
dataset = netCDF4.Dataset('http://tds.hycom.org/thredds/dodsC/datasets/GLBy0.08/expt_93.0/data/hindcasts/2019/hycom_glby_930_2019010112_t000_ts3z.nc')
lon = dataset.variables['lon']
lat = dataset.variables['lat']

lon_index_lower = index_strictly_lower(lon, os.getenv("MAP_LON_WEST"))
lon_index_upper = index_strictly_greater(lon, os.getenv("MAP_LON_EAST"))
lat_index_lower = index_strictly_lower(lat, os.getenv("MAP_LAT_SOUTH"))
lat_index_upper = index_strictly_greater(lat, os.getenv("MAP_LAT_NORTH"))
print(f"Latitude index:     {lat_index_lower} to {lat_index_upper}")
print(f"Longitude index:    {lon_index_lower} to {lon_index_upper}")

script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, 'config.env')

# Convert indices to strings
lon_index_lower_str = str(lon_index_lower)
lon_index_upper_str = str(lon_index_upper)
lat_index_lower_str = str(lat_index_lower)
lat_index_upper_str = str(lat_index_upper)

# Read file
with open(config_file, "r") as f:
    lines = f.readlines()

# Replace the lines
new_lines = []
for line in lines:
    if line.startswith("export MAP_LAT_INDEX_LOWER="):
        new_lines.append(f"export MAP_LAT_INDEX_LOWER={lat_index_lower_str}\n")
    elif line.startswith("export MAP_LAT_INDEX_UPPER="):
        new_lines.append(f"export MAP_LAT_INDEX_UPPER={lat_index_upper_str}\n")
    elif line.startswith("export MAP_LON_INDEX_LOWER="):
        new_lines.append(f"export MAP_LON_INDEX_LOWER={lon_index_lower_str}\n")
    elif line.startswith("export MAP_LON_INDEX_UPPER="):
        new_lines.append(f"export MAP_LON_INDEX_UPPER={lon_index_upper_str}\n")
    else:
        new_lines.append(line)

# Write back to config.env
with open(config_file, "w") as f:
    f.writelines(new_lines)

print("Updated config.env with new lat/lon index bounds.")

## see how to not repeat download dataset (it overlaps with hycom_grid.py)


# Verify the MATLAB and python scripts produce the same result; feel free to delete everything below this line
# mat = xr.open_dataset("straits.nc")
# py  = xr.open_dataset("straits_test.nc")

# print(np.allclose(mat["h"].values, py["h"].values, equal_nan=True))