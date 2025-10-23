import os

# Load config from environment
grid_id = os.getenv("PROJECT_NAME").upper()
grid_name = os.getenv("PROJECT_NAME")
grid_path = os.getenv("GRIDBUILDER_PATH")
grid_N = os.getenv("GRID_N")
grid_type = os.getenv("GRID_TYPE")
grid_vtrans = os.getenv("GRID_VTRANS")
theta_s = os.getenv("GRID_THETA_S")
theta_b = os.getenv("GRID_THETA_B")
tcline = os.getenv("GRID_TCLINE")

gridid_txt = os.path.expanduser('~/pyroms/pyroms/pyroms/gridid.txt') # need to make this relative to test_pyroms

# Read the current file, removes any empty lines so it will be written back without empty lines
with open(gridid_txt, 'r') as f:
    lines = [line for line in f.readlines() if line.strip() != '']

# Initialisation for parsing
preamble = []
blocks = []
current_block = []
in_block = False

# Parse file into preamble + blocks
# This section gives blocks in this format:
"""
#
id = xxx
...
#
"""
# Separate preamble dynamically
start_idx = 0
for i, line in enumerate(lines):
    if line.strip().startswith('id'):
        start_idx = i - 1  # include preceding '#' at start of block
        break
if start_idx == 0:
    print("No 'ID' found in gridid.txt")

# Preamble
for line in lines[:start_idx]:
    preamble.append(line)

# Blocks
for line in lines[start_idx:]:  # Skip preamble
    stripped = line.strip()
    if stripped.startswith('#'):
        if in_block:
            # End of block
            current_block.append(line)
            blocks.append(current_block)
            current_block = []
            in_block = False
        else:
            # Start of block
            in_block = True
            current_block.append(line)
    else:
        if in_block:
            current_block.append(line)

# Check if ID exists
existing_idx = None
for i, block in enumerate(blocks):
    for l in block: # Checks each line in a block for ID, nothing happens if no matching ID
        if l.strip().startswith('id') and '=' in l:
            block_id = l.split('=')[1].strip()
            if block_id.upper() == grid_id:
                existing_idx = i
                break
    if existing_idx is not None:
        break

# Prepare new block
new_block = ['#\n']
new_block.append(f"id      = {grid_id}\n")
new_block.append(f"name    = {grid_name}\n")
new_block.append(f"grdfile = {grid_path}\n")
new_block.append(f"N       = {grid_N}\n")
new_block.append(f"grdtype = roms\n")
new_block.append(f"Vtrans  = {grid_vtrans}\n")
new_block.append(f"theta_s = {theta_s}\n")
new_block.append(f"theta_b = {theta_b}\n")
new_block.append(f"Tcline  = {tcline}\n")
new_block.append('#\n')

# Update or append new block to the top; default option is to not overwrite
skip_flag = False
if existing_idx is not None:
    ans = input(f"Grid ID '{grid_id}' exists. Overwrite? [y/N]: ").lower()
    if ans == 'y':
        blocks[existing_idx] = new_block
        print(f"Overwritten grid ID '{grid_id}'.")
    else:
        print("Skipped update for existing grid ID.")
        skip_flag = True
else:
    blocks.insert(0, new_block)
    print(f"Added new grid ID '{grid_id}'.")

# Write to gridid.txt
with open(gridid_txt, 'w') as f:
    f.writelines(preamble)
    for b in blocks:
        f.writelines(b)

if skip_flag:
    print("No changes made to gridid.txt.")
else:
    print("gridid.txt updated successfully.")
