#!/bin/bash
set -e

# Change to the directory containing this script
script_dir=$(cd "$(dirname "$0")" && pwd)
cd "$script_dir"

echo -n "Choose a project name (alphanumeric and underscores only): "; read PROJ_NAME; echo ""

# Removes leading/trailing spaces and replaces spaces with underscores
PROJ_NAME=$(echo "$PROJ_NAME" | sed 's/^[ \t]*//;s/[ \t]*$//' | tr ' ' '_')

# Validate allowed characters: A-Z, a-z, 0-9, _
if [[ ! "$PROJ_NAME" =~ ^[A-Za-z0-9_]+$ ]]; then
    echo "Error: Invalid project name."
    echo "Allowed characters: letters, numbers and underscores (_) only."
    exit 1
fi

# Check for directory name conflict
if [ -d "$PROJ_NAME" ]; then
    echo "Error: Directory '$PROJ_NAME' already exists in this location."
    echo "Choose a different project name."
    exit 1
fi

cp -r template_project "$PROJ_NAME"
cd "$PROJ_NAME"

CONFIG_FILE="config.env"

if [ ! -f "${CONFIG_FILE}" ]; then
    echo "${CONFIG_FILE} not found. Please copy one in from the template folders."
    exit 1
else
    # Replace the existing PROJECT_NAME line
    sed -i "s|^export PROJECT_NAME=.*|export PROJECT_NAME='${PROJ_NAME}'|" "${CONFIG_FILE}"
fi

echo "New project created at: $script_dir/$PROJ_NAME"