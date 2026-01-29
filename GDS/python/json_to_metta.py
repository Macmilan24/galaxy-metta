import json
import os

# Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "../../data/raw/iwc_full.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "../metta/galaxy_data_full.metta")

# Sets to store unique atoms to avoid duplicates
nodes = set()
edges = set()


def clean_str(s):
    """Sanitize strings for MeTTa compatibility."""
    if not s:
        return "Unknown"
    # Replace quotes and newlines to avoid syntax errors
    return s.replace('"', "'").replace("\n", " ")


def add_node(name, type_label):
    if not name:
        return
    nodes.add(f'(: "{clean_str(name)}" {type_label})')


def add_edge(pred, source, target):
    if not source or not target:
        return
    edges.add(f'({pred} "{clean_str(source)}" "{clean_str(target)}")')


def process_workflow_data():
    print(f"Reading {JSON_PATH}...")
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    print("Processing graph...")

    for entry in data:
        cat_name = entry.get("category", "Uncategorized")
        add_node(cat_name, "Category")

        # Process Workflows
        for wf in entry.get("workflow_files", []):
            wf_name = wf.get("workflow_name", "Unnamed Workflow")
            add_node(wf_name, "Workflow")

            # Edge: Category -> Workflow
            add_edge("HAS_WORKFLOW", cat_name, wf_name)

            steps = wf.get("steps", {})
            step_map = {}
            if isinstance(steps, list):
                for s in steps:
                    step_map[s.get("step_id")] = s
            else:
                for k, v in steps.items():
                    step_map[v.get("step_id")] = v

            # Process Steps
            for step_id, step in step_map.items():
                # Create unique Step ID: WorkflowName_StepID
                step_unique_name = f"{wf_name}_Step_{step_id}"
                add_node(step_unique_name, "Step")
                add_edge("HAS_STEP", wf_name, step_unique_name)

                # Identify Tool
                tool_id = step.get("tool_id")
                if tool_id:
                    add_node(tool_id, "Tool")
                    add_edge("STEP_USES_TOOL", step_unique_name, tool_id)
                    add_edge("WORKFLOW_USES_TOOL", wf_name, tool_id)
                    add_edge("HAS_TOOL", cat_name, tool_id)  # Inferred category link

                    # Tool Inputs
                    for inp in step.get("inputs", []):
                        inp_name = inp.get("name")
                        add_node(inp_name, "ToolInput")
                        add_edge("TOOL_HAS_INPUT", tool_id, inp_name)

                    # Tool Outputs
                    for out in step.get("outputs", []):
                        out_name = out.get("name")
                        add_node(out_name, "ToolOutput")
                        add_edge("TOOL_HAS_OUTPUT", tool_id, out_name)

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
                        add_edge("FEEDS_INTO", src_unique_name, step_unique_name)

    # Write to File
    print(f"Writing {len(nodes)} nodes and {len(edges)} edges to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, "w") as f:
        f.write(";; Galaxy Knowledge Graph - Full Import\n\n")
        f.write(";; --- NODES ---\n")
        f.write("\n".join(sorted(nodes)))
        f.write("\n\n;; --- EDGES ---\n")
        f.write("\n".join(sorted(edges)))

    print("Done!")


if __name__ == "__main__":
    process_workflow_data()
