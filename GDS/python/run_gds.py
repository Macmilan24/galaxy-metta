import sys
import os
import time

# Ensure PeTTa libraries are importable
current_dir = os.path.dirname(os.path.abspath(__file__))
petta_path = os.path.abspath(os.path.join(current_dir, "../../PeTTa/python"))
if petta_path not in sys.path:
    sys.path.append(petta_path)

try:
    import petta
except ImportError:
    print(f"Error: Could not import 'petta' from {petta_path}")
    sys.exit(1)


def benchmark_load_time(data_file_path):
    """Loads a file into MORK via FFI and returns performance stats."""
    if not os.path.exists(data_file_path):
        print(f"Error: Data file not found at {data_file_path}")
        sys.exit(1)

    print(f"\n[Benchmark] Target Data: {os.path.basename(data_file_path)}")
    print("-" * 50)

    # 1. Read File IO
    t0 = time.time()
    with open(data_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    t1 = time.time()

    file_size_mb = len(content) / (1024 * 1024)
    read_duration = t1 - t0

    print(f"File Read:    {read_duration:.4f} sec ({file_size_mb:.2f} MB)")

    # 2. Parse & Load into Space
    if petta.janus is None:
        raise RuntimeError("Janus interface not initialized.")

    t2 = time.time()
    try:
        # Direct FFI call to MORK Rust backend
        # 'mork' predicate maps to rust_mork function in libmork_ffi.so
        resp = petta.janus.query_once(
            "mork('add-atoms', Content, Result)", {"Content": content}
        )
        if not resp or "OK" not in str(resp.get("Result")):
            raise RuntimeError(f"MORK Load Failed: {resp}")

    except Exception as e:
        print(f"CRITICAL ERROR during MORK load: {e}")
        sys.exit(1)

    t3 = time.time()
    load_duration = t3 - t2

    print(f"MORK Ingest:  {load_duration:.4f} sec")
    print(f"Total Time:   {t3 - t0:.4f} sec")


def run_metta_script(agent, filepath):
    """Executes a MeTTa script using the PeTTa agent."""
    if not os.path.exists(filepath):
        return

    filename = os.path.basename(filepath)
    print(f"\n[Running] {filename}...")

    t_start = time.time()
    results = agent.load_metta_file(filepath)
    t_end = time.time()

    if results:
        for r in results:
            print(f"  > {r}")

    print(f"  Finished in {t_end - t_start:.4f} sec")


def main():
    print("Initializing PeTTa Environment...")
    agent = petta.PeTTa(verbose=False)

    # Paths
    data_file = os.path.abspath(
        os.path.join(current_dir, "../metta/galaxy_data_full.metta")
    )
    schema_file = os.path.abspath(
        os.path.join(current_dir, "../metta/galaxy_schema.metta")
    )
    queries_file = os.path.abspath(
        os.path.join(current_dir, "../metta/galaxy_queries.metta")
    )

    # Execute Pipeline
    benchmark_load_time(data_file)
    run_metta_script(agent, schema_file)
    run_metta_script(agent, queries_file)

    print("-" * 50)
    print("Execution Complete.")


if __name__ == "__main__":
    main()
