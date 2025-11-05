#!/bin/bash
# =========================================================
# setup_conda_env_pyroms.sh
# Create the pyroms conda environment and update config.env
# =========================================================

set -e  # Exit immediately if any command fails

# --- Step 1. Check for conda installation ---
if ! command -v conda &>/dev/null; then
    echo "Error: Conda not found. Please install Miniconda or Anaconda first from:"
    echo 'https://docs.conda.io/projects/conda/en/stable/user-guide/install/linux.html#installing-on-linux'
    exit 1
fi

# --- Step 2. Prompt for environment name ---
DEFAULT_ENV="pyroms-py38"
read -p "Choose a conda environment name [alphanumeric and hyphens only; default name is ${DEFAULT_ENV}]: " USER_ENV
USER_ENV=$(echo "${USER_ENV}" | sed 's/^[ \t]*//;s/[ \t]*$//' | tr ' ' '-')
ENV_NAME=${USER_ENV:-$DEFAULT_ENV}

echo "Using conda environment name: ${ENV_NAME}"

# --- Step 3. Create or update the environment ---
if [ ! -f environment.yaml ]; then
    echo "Error: environment.yaml not found in the current directory. Please copy one in from the template folders."
    exit 1
fi

echo "Creating conda environment from environment.yaml..."
# Commented out for testing, uncomment when ready
conda env create -n "${ENV_NAME}" -f environment.yaml || {
    echo "Environment ${ENV_NAME} may already exist. Attempting update..."
    conda env update -n "${ENV_NAME}" -f environment.yaml
}

echo "Conda environment '${ENV_NAME}' is ready."

conda activate "${ENV_NAME}"

# --- Step 4. Update config.env ---
# CONFIG_FILE="config.env"

# if [ ! -f "${CONFIG_FILE}" ]; then
#     echo "${CONFIG_FILE} not found. Please copy one in from the template folders."
#     exit 1
# else
#     # Replace the existing PYROMS_CONDA_ENV line
#     sed -i "s|^export PYROMS_CONDA_ENV=.*|export PYROMS_CONDA_ENV='${ENV_NAME}'|" "${CONFIG_FILE}"
# fi

# echo "Updated ${CONFIG_FILE} with:"
# echo "    export PYROMS_CONDA_ENV='${ENV_NAME}'"

echo
echo "Setup complete."
echo "To activate your environment, run:"
echo "    conda activate ${ENV_NAME}"
echo "To deactivate your environment, run:"
echo "    conda deactivate"
echo "To see all installed environments, run:"
echo "    conda env list"
echo "To remove your environment, run:"
echo "    conda env remove -n ${ENV_NAME}"
echo ""
echo "Additionally, ensure you have ksh and ncks installed by running:"
echo "sudo apt install ksh nco"

# echo -e '
# meow  |\__/,|   (`\
#     _.|o o  |_   ) )
# ---(((---(((---------
# '