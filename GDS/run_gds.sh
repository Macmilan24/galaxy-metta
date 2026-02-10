#!/bin/bash

LOG_FILE="gds_output.log"
SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" && pwd)

# Locate the compiled Rust MORK library for direct FFI access
MORK_LIB="$(readlink -f "$SCRIPT_DIR/../PeTTa/mork_ffi/target/release/libmork_ffi.so")"

if [ ! -f "$MORK_LIB" ]; then
    echo "Error: MORK library not found at $MORK_LIB"
    echo "Please build PeTTa/MORK first."
    exit 1
fi

echo "Running GDS with high-performance MORK loader..."
echo "Using Library: $MORK_LIB"

# Pass arguments ("$@") to the python script so flags work
LD_PRELOAD="$MORK_LIB" python3 python/run_gds.py "$@" | tee "$LOG_FILE"