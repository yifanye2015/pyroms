import os
import subprocess
from datetime import datetime

# Date range information
year = int(os.getenv("YEAR"))
start_date = os.getenv("MERRA2_START_DATE")
end_date = os.getenv("MERRA2_END_DATE")

# Date range processing
start_month = int(start_date[0:2])
end_month = int(end_date[0:2])

# Variable names
varnames = ['Pair', 'Qair', 'Tair', 'Uwind', 'Vwind', 'swrad', 'lwrad_down', 'cloud', 'rain', 'snow', 'albedo']
var_freq_patterns = [f"{varname}_{'daily' if varname == 'albedo' else '3hours'}" for varname in varnames]
# ['Pair_3hours', 'Qair_3hours', 'Tair_3hours', 'Uwind_3hours', 'Vwind_3hours', 'swrad_3hours', 'lwrad_down_3hours', 'cloud_3hours', 'rain_3hours', 'snow_3hours', 'albedo_daily']

# Set directories
output_dir = "../output_files/merra2_opendap_files/Forcings"

for var_freq_pattern in var_freq_patterns:
    for month_val in range(start_month, end_month + 1):
        month = f"{month_val:02d}"
        print(f"Processing {var_freq_pattern}_{year}_{month}...")

        # Define naming patterns
        output_file = os.path.join(output_dir, f"MERRA2_{var_freq_pattern}_{year}_{month}.nc")
        
        # Use glob pattern to find all days in that month
        # This matches MERRA2_varname_3hours_yyyy_mm01.nc through mm31.nc for example
        input_pattern = f"Forcings/MERRA2_{var_freq_pattern}_{year}_{month}??.nc"
        
        # Construct the command
        # We use shell=True to allow the wildcard (?) to be expanded by the shell
        # ncrcat only works for unlimited dimensions
        # can check using xarray: ds.encoding should contain {'unlimited_dims': {'var_time'}}
        cmd = f"ncrcat -O {input_pattern} {output_file}"
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"Successfully created {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing month {month}: {e}")