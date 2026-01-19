import os
from hyperon import MeTTa

def main():
    # 1. Initialize MeTTa
    metta = MeTTa()
    
    # 2. Define Paths relative to this script
    # This script is in src/python/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Types are in src/metta/types.metta
    types_path = os.path.join(base_dir, "../metta/types.metta")
    
    # Data is in data/knowledge_base.metta
    data_path = os.path.join(base_dir, "../../data/knowledge_base.metta")

    print(f"🔹 Loading Types from: {types_path}")
    with open(types_path, 'r') as f:
        metta.run(f.read())

    print(f"🔹 Loading Knowledge Base from: {data_path}")
    # We use import_file which handles large files better than reading into string
    try:
        # Note: In Python MeTTa, we often load content directly or use import logic
        # For simplicity with large files, we can instruct the runner to load it
        runner = metta.run(f'!(import! &self "{data_path}")')
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return

    # 3. Run Checks
    print("\n--- Running Queries ---")
    
    query_1 = "!(match &self (used-in $t $w) (found-edge $t $w))"
    print(f"Running: {query_1}")
    result1 = metta.run(query_1)
    # Print just the first few results to avoid flooding screen
    print(f"Result (First 5): {result1[0][:5]}...")

    query_2 = "!(match &self (used-in (Tool compose_text_param) $w) (found-tool-in $w))"
    print(f"\nChecking for compose_text_param: {query_2}")
    result2 = metta.run(query_2)
    print(f"Result: {result2}")

if __name__ == "__main__":
    main()