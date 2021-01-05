#!/bin/bash

FULL_PATH_TO_SCRIPT="$(realpath "$0")"

# You can then also get the full path to the directory, and the base
# filename, like this:
SCRIPT_DIRECTORY="$(dirname "$FULL_PATH_TO_SCRIPT")"
SCRIPT_FILENAME="$(basename "$FULL_PATH_TO_SCRIPT")"


echo $SCRIPT_DIRECTORY 
