import os
from hyperon import MeTTa

def main():
    print("🔹 Initializing MeTTa Hypergraph System...")
    metta = MeTTa()
    
    # 1. Define Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    metta_dir = os.path.join(base_dir, "../metta")
    data_dir = os.path.join(base_dir, "../../data")
    
    utils_path = os.path.join(metta_dir, "utils.metta")
    kb_path = os.path.join(data_dir, "knowledge_base.metta")
    algo_path = os.path.join(metta_dir, "algo.metta")

    # 2. Load UTILITIES (Directly into memory)
    print(f"🔹 Loading Logic: {utils_path}")
    try:
        with open(utils_path, 'r') as f:
            metta.run(f.read())
    except FileNotFoundError:
        print(f"❌ Error: {utils_path} not found.")
        return

    # 3. Load KNOWLEDGE BASE (Directly into memory)
    # This bypasses any size limits or path issues with 'import!'
    print(f"🔹 Loading Data: {kb_path} (This might take a few seconds)...")
    try:
        with open(kb_path, 'r') as f:
            metta.run(f.read())
    except FileNotFoundError:
        print(f"❌ Error: {kb_path} not found. Did you run converter.py?")
        return

    # 4. Load ALGORITHM (With Import Stripping)
    # We must read the file, REMOVE the (import! ...) lines (since we already loaded them),
    # and then run the rest.
    print(f"🔹 Running Community Detection: {algo_path}")
    try:
        with open(algo_path, 'r') as f:
            algo_lines = f.readlines()
            
        # Filter out lines that try to import files, to prevent errors
        clean_code = []
        for line in algo_lines:
            if "import!" not in line:
                clean_code.append(line)
                
        # Run the cleaned code
        results = metta.run("".join(clean_code))
        
    except FileNotFoundError:
        print(f"❌ Error: {algo_path} not found.")
        return

    # 5. Process Results
    print("🔹 Processing Social Dynamics...")
    
    influence_scores = {}
    flat_results = []
    
    if results:
        for result_set in results:
            for atom in result_set:
                flat_results.append(atom)
    
    print(f"🔹 Received {len(flat_results)} output atoms from MeTTa.")

    for atom in flat_results:
        atom_str = str(atom)
        
        # Check for Errors
        if atom_str.startswith("(Error"):
            print(f"⚠️  MeTTa Runtime Error: {atom_str}")
            continue

        # Look for Influence tuples
        if atom_str.startswith("(Influence"):
            try:
                # Format: "(Influence tool_name (neighbor1 neighbor1 ...))"
                cleaned = atom_str.replace("(Influence ", "").strip("()")
                
                parts = cleaned.split(' ', 1)
                if len(parts) < 2: 
                    continue 
                    
                tool_name = parts[0]
                neighbors_blob = parts[1]
                
                # Count Neighbors
                neighbors_clean = neighbors_blob.replace("(", "").replace(")", "")
                neighbor_list = neighbors_clean.split()
                count = len(neighbor_list)
                
                influence_scores[tool_name] = count
                
            except Exception as e:
                continue

    # --- DISPLAY RESULTS ---
    print("\n" + "="*60)
    print(f"{'GALAXY TOOL':<40} | {'INFLUENCE (DEGREE)':<15}")
    print("="*60)
    
    if not influence_scores:
        print("❌ No Influence data found.")
    else:
        sorted_tools = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)
        
        for tool, score in sorted_tools[:30]: 
            display_name = tool[:38]
            print(f"{display_name:<40} | {score:<15}")
            
        print("="*60)
        print(f"Total Tools Analyzed: {len(influence_scores)}")

if __name__ == "__main__":
    main()