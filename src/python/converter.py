import json
import os
import re

INPUT_FILE = "../../data/raw/iwc_full.json"
OUTPUT_FILE = "../../data/knowledge_base.metta"

def clean_symbol(text):
    """
    Converts a string into a valid MeTTa symbol.
    Ex: "Bacterial Genome Annotation" -> "Bacterial_Genome_Annotation"
    """
    
    if text is None: return "unknown"
    
    clean = re.sub(r'[^a-zA-Z0-9]', '_', text)
    clean = re.sub(r'[^a-zA-Z0-9]', '_', text)
    
    return clean.strip("_")

def extract_tool_name(tool_id):
    """
    Parses Galaxy Tool IDs to get the canonical name.
    Input: "toolshed.g2.bx.psu.edu/repos/iuc/bakta/bakta/1.9.4+galaxy1"
    Output: "bakta"
    """
    if not tool_id: return None
    
    parts = tool_id.split('/')
    
    if len(parts) > 2:
        if any(char.isdigit() for char in parts[-1]):
            candidate = parts[-2]
        else:
            candidate = parts[-1]
        
        return clean_symbol(candidate)
    
    return clean_symbol(tool_id)

def convert_json_to_metta():
    print(f"🔹 Reading {INPUT_FILE}...")
    
    try:
        with open(INPUT_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found at {INPUT_FILE}")
        return
    
    metta_output = [
         ";; ============================================================",
        ";; GENERATED KNOWLEDGE BASE",
        ";; Source: iwc_full.json",
        ";; ============================================================",
        ""
    ]  
    repositories = data if isinstance(data, list) else [data]
    
    total_edges = 0
    total_workflows = 0
    
    print(f"🔹 Found {len(repositories)} repositories/categories to process.")
    
    for repo in repositories:
        
        workflows = repo.get("workflow_files", [])
        
        for wf in workflows:
            wf_name_raw = wf.get("workflow_name", "Unnamed")
            wf_symbol = clean_symbol(wf_name_raw)
            
            if wf_symbol == "Unnamed" or not wf_symbol:
                continue
            
            metta_output.append(f";; Workflow: {wf_name_raw}")
            total_workflows += 1
            
            steps = wf.get("steps",[])
            
            seen_tools = set()
            
            for step in steps:
                if step.get("type") == "tool":
                    tool_id_raw = step.get("tool_id")
                    tool_name = step.get("name")
                    
                    
                    canonical_id = extract_tool_name(tool_id_raw) or clean_symbol(tool_name)
                    
                    if canonical_id and canonical_id not in seen_tools:
                        edge = f"(used-in (Tool {canonical_id}) (Workflow {wf_symbol}))"
                        metta_output.append(edge)
                        
                        seen_tools.add(canonical_id)
                        total_edges += 1
            
            metta_output.append("")
        
    with open(OUTPUT_FILE, 'w') as f:
        f.write("\n".join(metta_output))

    print(f"✅ Conversion Complete.")
    print(f"🔹 Extracted {total_edges} Tool-Workflow relationships.")
    print(f"🔹 Saved to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    convert_json_to_metta()
    