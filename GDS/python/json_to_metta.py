import hashlib
import json
import os
import re

# Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "../../data/raw/iwc_full.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "../metta/galaxy_data_full.metta")


def clean_label(s):
    """
    Sanitizes a string to ensure it is safe for use as a MeTTa symbol value.
    Removes newlines, tabs, and escapes special characters.
    """
    if not s:
        return "Unknown"
    s = s.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    s = s.replace("\\", "/")
    s = s.replace('"', '\\"')
    s = "".join(ch if ch >= " " else " " for ch in s)
    return s


def to_symbol(s, prefix):
    """
    Converts an arbitrary string into a valid, unique MeTTa identifier symbol.
    Uses a prefix and an MD5 hash suffix to ensure uniqueness and validity.
    """
    if not s:
        return f"{prefix}_unknown"

    # Remove invalid characters for MeTTa symbols
    base = clean_label(s)
    base = re.sub(r"[^A-Za-z0-9_]+", "_", base).strip("_")
    if not base:
        base = "unknown"

    # Ensure it doesn't start with a digit
    if base[0].isdigit():
        base = f"{prefix}_{base}"

    # Append hash to prevent collisions between similar names
    h = hashlib.md5(s.encode("utf-8", errors="ignore")).hexdigest()[:8]
    if len(base) > 72:
        base = base[:72]
    return f"{base}_{h}"


def add_node(out, name, type_label):
    """
    Writes a node definition to the output file in MeTTa format.
    Example: (: symbol Type)
    """
    if not name:
        return
    node_sym = to_symbol(name, type_label.lower())
    out.write(f"(: {node_sym} {type_label})\n")


def add_edge(out, pred, source, target):
    """
    Writes a relationship (edge) between two nodes to the output file.
    Example: (PREDICATE source_node target_node)
    """
    if not source or not target:
        return
    src_sym = to_symbol(source, "node")
    tgt_sym = to_symbol(target, "node")
    out.write(f"({pred} {src_sym} {tgt_sym})\n")


def process_workflow_data():
    """
    Main processing pipeline.
    Reads the raw JSON dataset, extracts entities and relationships,
    and writes the complete knowledge graph to a .metta file.
    """
    print(f"Reading {JSON_PATH}...")
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    print("Processing graph...")
    print(f"Writing to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, "w") as out:
        out.write(";; Galaxy Knowledge Graph - Full Import\n\n")
        out.write(";; --- ATOMS ---\n")

        # Iterate over categories in the JSON
        for entry in data:
            cat_name = entry.get("category", "Uncategorized")
            add_node(out, cat_name, "Category")

            # Process Workflows within each category
            for wf in entry.get("workflow_files", []):
                wf_name = wf.get("workflow_name", "Unnamed Workflow")
                add_node(out, wf_name, "Workflow")

                # Edge: Category -> Workflow
                add_edge(out, "HAS_WORKFLOW", cat_name, wf_name)

                # Normalize 'steps' since it can be a list or dict in source
                steps = wf.get("steps", {})
                step_map = {}
                if isinstance(steps, list):
                    for s in steps:
                        step_map[s.get("step_id")] = s
                else:
                    for k, v in steps.items():
                        step_map[v.get("step_id")] = v

                # Create nodes for each Step in the workflow
                for step_id, step in step_map.items():
                    # Create unique Step ID: WorkflowName_StepID
                    step_unique_name = f"{wf_name}_Step_{step_id}"
                    add_node(out, step_unique_name, "Step")
                    add_edge(out, "HAS_STEP", wf_name, step_unique_name)

                    # Identify Tool
                    tool_id = step.get("tool_id")
                    if tool_id:
                        add_node(out, tool_id, "Tool")
                        add_edge(out, "STEP_USES_TOOL", step_unique_name, tool_id)
                        add_edge(out, "WORKFLOW_USES_TOOL", wf_name, tool_id)
                        add_edge(out, "HAS_TOOL", cat_name, tool_id)

                        # Tool Inputs
                        for inp in step.get("inputs", []):
                            inp_name = inp.get("name")
                            add_node(out, inp_name, "ToolInput")
                            add_edge(out, "TOOL_HAS_INPUT", tool_id, inp_name)

                        # Tool Outputs
                        for out_item in step.get("outputs", []):
                            out_name = out_item.get("name")
                            add_node(out, out_name, "ToolOutput")
                            add_edge(out, "TOOL_HAS_OUTPUT", tool_id, out_name)

                    # Process Connections (The Flow)
                    # "input_connections": { "input_name": { "id": source_step_id, ... } }
                    conns = step.get("input_connections", {})
                    for conn_name, source_info in conns.items():
                        # source_info might be a list or dict
                        if isinstance(source_info, dict):
                            src_id = source_info.get("id")
                        elif isinstance(source_info, list) and len(source_info) > 0:
                            src_id = source_info[0].get("id")
                        else:
                            continue

                        if src_id is not None:
                            src_unique_name = f"{wf_name}_Step_{src_id}"
                            # Edge: Source Step -> This Step
                            add_edge(
                                out, "FEEDS_INTO", src_unique_name, step_unique_name
                            )

    print("Done!")


if __name__ == "__main__":
    process_workflow_data()
