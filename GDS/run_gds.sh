#!/bin/bash

# Define a temporary file to hold the combined code
COMBINED_FILE="metta/galaxy_full_run.metta"

cat metta/galaxy_schema.metta metta/galaxy_data_full.metta metta/galaxy_queries.metta > "$COMBINED_FILE"

sh ../PeTTa/run.sh "$COMBINED_FILE" --silent \
  | grep -vE "^-->|^\^\^\^\^\^|:- findall"

# 3. Clean up the temporary file
rm "$COMBINED_FILE"