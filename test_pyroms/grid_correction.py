import xarray as xr
import numpy as np
import os

# Path to the grid file
local_grid = os.getenv("GRIDBUILDER_PATH")

# Load the dataset
ds = xr.open_dataset(local_grid)

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

# Verify the MATLAB and python scripts produce the same result; feel free to delete everything below this line
# mat = xr.open_dataset("straits.nc")
# py  = xr.open_dataset("straits_test.nc")

# print(np.allclose(mat["h"].values, py["h"].values, equal_nan=True))