import os
import time
from hyperon import MeTTa

# --- CONFIGURATION ---
HUB_THRESHOLD = 80


def format_time(seconds):
    """Returns a clean string for time (ms or s)"""
    if seconds < 1.0:
        return f"{seconds * 1000:.2f} ms"
    return f"{seconds:.4f} s"


def main():

    t_start = time.time()

    print("🔹 Initializing MeTTa Hypergraph Engine...")
    metta = MeTTa()

    # Path Setup
    base_dir = os.path.dirname(os.path.abspath(__file__))
    metta_dir = os.path.join(base_dir, "../metta")
    data_dir = os.path.join(base_dir, "../../data")

    utils_path = os.path.join(metta_dir, "utils.metta")
    kb_path = os.path.join(data_dir, "knowledge_base.metta")
    algo_path = os.path.join(metta_dir, "algo.metta")

    t_init = time.time()

    print("🔹 Loading Knowledge Base & Logic...")
    try:
        with open(utils_path, "r") as f:
            metta.run(f.read())
        with open(kb_path, "r") as f:
            metta.run(f.read())

        # Load algo stripping imports
        with open(algo_path, "r") as f:
            algo_lines = [l for l in f.readlines() if "import!" not in l]

    except FileNotFoundError as e:
        print(f"❌ Critical Error: {e}")
        return

    t_load = time.time()

    print("🔹 Executing Hypergraph Analysis (Label Propagation)...")
    results = metta.run("".join(algo_lines))

    t_algo = time.time()

    print("🔹 Processing & Filtering Results...")

    influence_scores = {}
    flat_results = [atom for res in results for atom in res]

    for atom in flat_results:
        atom_str = str(atom)
        if atom_str.startswith("(Influence"):
            try:
                cleaned = atom_str.replace("(Influence ", "").strip("()")
                parts = cleaned.split(" ", 1)
                if len(parts) < 2:
                    continue

                tool = parts[0]
                # Count neighbors
                deg = len(parts[1].replace("(", "").replace(")", "").split())
                influence_scores[tool] = deg
            except:
                continue

    # Clustering Logic
    communities = {}
    hubs = []

    for tool, score in influence_scores.items():
        if score > HUB_THRESHOLD:
            hubs.append((tool, score))
        else:
            if score not in communities:
                communities[score] = []
            communities[score].append(tool)

    t_process = time.time()

    # --- GENERATE REPORT ---
    print("\n" + "=" * 60)
    print("🧬 GALAXY HYPERGRAPH COMMUNITY REPORT 🧬")
    print("=" * 60)
    print(f"Total Tools: {len(influence_scores)}")
    print(f"Hubs Filtered Out (> {HUB_THRESHOLD}): {len(hubs)}")

    print("\n--- 🌐 DETECTED FUNCTIONAL MODULES ---")

    sorted_comms = sorted(communities.items(), key=lambda x: x[0], reverse=True)

    for score, tools in sorted_comms:
        if len(tools) >= 2:
            print(f"\n[🔗 Connectivity Score: {score}]")
            print(f"  Members: {', '.join(tools)}")
            prefixes = [t.split("_")[0] for t in tools]
            common_tag = max(set(prefixes), key=prefixes.count)
            print(f"  👉 Likely Domain: {common_tag.upper()} Workflow")

    # --- BENCHMARK SUMMARY ---
    print("\n" + "=" * 60)
    print("🚀 PERFORMANCE BENCHMARK (Hyperon-Experimental)")
    print("=" * 60)

    time_init = t_init - t_start
    time_load = t_load - t_init
    time_algo = t_algo - t_load
    time_proc = t_process - t_algo
    total_time = t_process - t_start

    print(f"1. System Init:      {format_time(time_init)}")
    print(f"2. Data Loading:     {format_time(time_load)}  (Parsing Atoms)")
    print(f"3. MeTTa Inference:  {format_time(time_algo)}  (Pattern Matching)")
    print(f"4. Python Filtering: {format_time(time_proc)}  (Sorting/Reporting)")
    print("-" * 60)
    print(f"✅ TOTAL RUNTIME:    {format_time(total_time)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
