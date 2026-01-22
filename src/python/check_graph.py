import os
from hyperon import MeTTa


def main():
    # 1. Initialize MeTTa
    metta = MeTTa()

    # 2. Define Paths relative
    base_dir = os.path.dirname(os.path.abspath(__file__))

    types_path = os.path.join(base_dir, "../metta/types.metta")

    data_path = os.path.join(base_dir, "../../data/knowledge_base.metta")

    print(f"🔹 Loading Types from: {types_path}")
    with open(types_path, "r") as f:
        metta.run(f.read())

    print(f"🔹 Loading Knowledge Base from: {data_path}")
    try:
        runner = metta.run(f'!(import! &self "{data_path}")')
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return

    # 3. Run Checks
    print("\n--- Running Queries ---")

    query_1 = "!(match &self (used-in $t $w) (found-edge $t $w))"
    print(f"Running: {query_1}")
    result1 = metta.run(query_1)
    # Print just the first few results
    print(f"Result (First 5): {result1[0][:5]}...")

    query_2 = "!(match &self (used-in (Tool compose_text_param) $w) (found-tool-in $w))"
    print(f"\nChecking for compose_text_param: {query_2}")
    result2 = metta.run(query_2)
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
