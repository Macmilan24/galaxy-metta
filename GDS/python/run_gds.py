import sys
import os
import time
import json
import argparse
import statistics
from collections import Counter

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
    """
    Loads the dataset into the MORK runtime via FFI.
    Measures and reports the time taken for file I/O and MORK ingestion.
    """
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


def process_gds_results(results):
    """
    Parses complex GDS query results to generate a comprehensive JSON report.
    """
    print("\n[Processing GDS Report]...")

    # Storage for raw values
    raw_degrees = []
    raw_lcc = []
    hubs = []
    triangle_count = 0
    opentriad_count = 0

    # 1. Parse Results
    for r in results:
        r_str = str(r)

        # --- Degree Parsing ---
        if "Degree of" in r_str:
            try:
                # Clean up formatting
                cleaned_str = (
                    r_str.replace('"', "")
                    .replace("'", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace(",", "")
                )
                parts = cleaned_str.split()
                # We expect the last part to be the numeric value
                if len(parts) >= 1:
                    val = parts[-1]
                    raw_degrees.append(int(val))
            except (ValueError, TypeError):
                pass

        # --- Clustering Coefficient (LCC) Parsing ---
        elif "LCC of" in r_str:
            try:
                cleaned_str = (
                    r_str.replace('"', "")
                    .replace("'", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace(",", "")
                )
                parts = cleaned_str.split()
                if len(parts) >= 1:
                    val = parts[-1]
                    raw_lcc.append(float(val))
            except (ValueError, TypeError):
                pass

        # --- Motifs: Triangles ---
        # Look for atom structure (Triangle A B C)
        elif "Triangle" in r_str and "Motif:" not in r_str:
            cleaned = r_str.strip().lstrip("(").lstrip('"')
            if cleaned.startswith("Triangle"):
                triangle_count += 1

        # --- Motifs: Open Triads ---
        elif "OpenTriad" in r_str and "Motif:" not in r_str:
            opentriad_count += 1

        # --- Hubs ---
        elif "Hub" in r_str:
            try:
                cleaned_str = (
                    r_str.replace('"', "")
                    .replace("'", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace(",", "")
                )
                parts = cleaned_str.split()

                # Look for 'Degree' keyword
                if "Degree" in parts:
                    idx = parts.index("Degree")
                    if idx + 1 < len(parts):
                        degree_val = int(parts[idx + 1])
                        node_name = parts[1] if len(parts) > 1 else "unknown"
                        hubs.append({"node": node_name, "degree": degree_val})
            except Exception:
                pass

    # 2. Build JSON Structure

    # -- Degree Section --
    degree_data = {}
    if raw_degrees:
        counts = Counter(raw_degrees)
        sorted_degrees = sorted(counts.keys())
        degree_data["bins"] = [
            {"degree": d, "frequency": counts[d]} for d in sorted_degrees
        ]
        print(f"  > Processed {len(raw_degrees)} degree records.")

    # -- Clustering Section --
    clustering_data = {}
    if raw_lcc:
        clustering_data["local"] = {
            "avg": statistics.mean(raw_lcc),
            "min": min(raw_lcc),
            "max": max(raw_lcc),
            "p50": statistics.median(raw_lcc),
        }
        if len(raw_lcc) > 1:
            clustering_data["local"]["stdev"] = statistics.stdev(raw_lcc)

        # Simple Global estimation (Transitivity)
        if (triangle_count + opentriad_count) > 0:
            total_triplets = opentriad_count + (3 * triangle_count)
            clustering_data["global"] = (
                (3 * triangle_count) / total_triplets if total_triplets > 0 else 0.0
            )

        print(f"  > Processed {len(raw_lcc)} LCC records.")

    # -- Motifs Section --
    motifs_data = {
        "triangles": triangle_count,
        "triangles_unique_approx": int(triangle_count / 6),
        "openTriads": opentriad_count,
        "hubs": sorted(hubs, key=lambda x: x["degree"], reverse=True),
    }
    print(
        f"  > Found {triangle_count} triangle instances (approx {int(triangle_count/3)} unique)."
    )

    # Final Assembly
    metrics = {
        "degree": degree_data,
        "clustering": clustering_data,
        "motifs": motifs_data,
        # "blocks": {...} (Communities omitted as requested)
    }

    # 3. Export
    json_path = "gds_metrics.json"
    try:
        with open(json_path, "w") as f:
            json.dump(metrics, f, indent=2)
        print(f"\n[Success] Full GDS Metrics saved to: {os.path.abspath(json_path)}")

        # Print a short stdout summary for immediate feedback
        if raw_degrees:
            print("\n  [Degree Distribution Preview]")
            print(f"  {'Degree':<10} | {'Frequency':<10}")
            print("  " + "-" * 25)
            # Show first 5
            c = Counter(raw_degrees)
            for d in sorted(c.keys())[:5]:
                print(f"  {d:<10} | {c[d]:<10}")
            if len(c) > 5:
                print("  ...")

    except Exception as e:
        print(f"[Error] Failed to write JSON: {e}")


def run_metta_script(agent, filepath, report_type="detailed"):
    """
    Executes a specific MeTTa script file using the PeTTa agent.
    Handles output formatting based on the user's report preference (detailed vs summary).
    """
    if not os.path.exists(filepath):
        return

    filename = os.path.basename(filepath)
    print(f"\n[Running] {filename}...")

    t_start = time.time()
    results = agent.load_metta_file(filepath)
    t_end = time.time()

    if results:
        if report_type == "summary" and "galaxy_queries" in filename:
            process_gds_results(results)
        else:
            # Default behavior: Print every result line-by-line
            for r in results:
                print(f"  > {r}")

    print(f"  Finished in {t_end - t_start:.4f} sec")


def main():
    """
    Entry point for the GDS pipeline.
    Parses arguments, initializes the environment, and runs the benchmark and query execution steps.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        choices=["detailed", "summary"],
        default="detailed",
        help="Choose 'detailed' for list of all nodes, or 'summary' for grouped counts.",
    )
    # Parse the arguments
    args = parser.parse_args()

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
    run_metta_script(agent, schema_file, report_type=args.report)
    run_metta_script(agent, queries_file, report_type=args.report)


if __name__ == "__main__":
    main()
