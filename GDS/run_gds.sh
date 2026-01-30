#!/bin/bash

# Define a temporary file to hold the combined code
COMBINED_FILE="metta/galaxy_full_run.metta"

cat metta/galaxy_schema.metta metta/galaxy_data_full.metta metta/galaxy_queries.metta > "$COMBINED_FILE"

LOG_FILE="gds_output.log"
sh ../PeTTa/run.sh "$COMBINED_FILE" --silent \
  | grep -vE "^-->|^\^\^\^\^\^|:- findall"\
  | tee "$LOG_FILE"

# 3. Clean up the temporary file
rm "$COMBINED_FILE"