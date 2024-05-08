#!/bin/bash

valid_args=("--analysis_only" "--dataset_only" "--skip_station_data")

is_valid_arg() {
    local arg=$1
    for valid_arg in "${valid_args[@]}"; do
        if [[ $arg == "$valid_arg" ]]; then
            return 0
        fi
    done
    return 1
}

for arg in "$@"; do
    if ! is_valid_arg "$arg"; then
        echo "Invalid argument: $arg"
        echo "Usage: ./run.sh --analysis_only | --dataset_only | --skip_station_data"
        exit 1
    fi
done

source .venv/bin/activate
python3 main.py "$@"
