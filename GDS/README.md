# Galaxy Graph Data Science (GDS) in MeTTa

This directory contains the Graph Data Science implementation for the Galaxy Knowledge Graph using Hyperon (MeTTa). It replicates standard Neo4j GDS algorithms purely in MeTTa logic.

## Directory Structure

```
GDS/
├── metta/
│   ├── galaxy_data.metta       # Sample dataset (small scale)
│   ├── galaxy_schema.metta     # Type definitions and Schema
│   ├── galaxy_queries.metta    # The GDS Algorithms implementation
│   └── galaxy_data_full.metta  # Full dataset (generated from JSON)
├── python/
│   └── json_to_metta.py        # Script to convert raw Galaxy JSON to MeTTa atoms
└── run_gds.sh                  # Helper script to run the queries
```

## Implemented Algorithms

### 1. Connectivity & Degree
Calculates the "Natural" degree of nodes (Undirected sum of edges).
- **Purpose**: Identify "hub" nodes (super-connectors) like popular tools or central workflows.
- **Logic**: Counts all incoming and outgoing edges defined in the GDS projection.

### 2. Local Clustering Coefficient (LCC)
Measures the "cliquishness" of a node's neighborhood.
- **Formula**: `LCC = Actual Triangles / Possible Triangles`
- **Purpose**: Determine if tools are used in tight-knit groups (communities) or independently.

### 3. Motif Analysis
Searches for specific geometric shapes in the graph.
- **Triangles**: `A-B-C-A` (Closed loops). Represents tightly integrated tool chains.
- **Open Triads**: `A-B-C` where `A` is NOT connected to `C`. Represents potential recommendation opportunities.

## Usage

### 1. Generate Full Data
First, convert the raw JSON data into pre-optimized MeTTa S-expressions:
```bash
python3 python/json_to_metta.py
```

### 2. Run GDS Pipeline
Run the high-performance loader which injects data directly into the MORK backend:
```bash
./run_gds.sh
```

**Options:**
- **Standard Output** (Default): Prints detailed results line-by-line.
- **Summary Report**: Generates a statistical summary (histograms, motif counts) and saves a JSON report.
  ```bash
  ./run_gds.sh --report summary
  ```

This script performs the following steps:
1.  **Benchmarks** the data ingest speed (Python Read -> Rust FFI -> MORK Space).
2.  Loads the **Schema** definitions.
3.  Executes the **GDS Algorithms** (queries).


### Slow Performance
**Symptom**: Queries take >30 seconds

**Check**:
1. Is MORK backend enabled? (Check for "mork" in run.sh command)
2. Are symbols >64 bytes? (Check data file)
3. Is the data file corrupted? (Regenerate with json_to_metta.py)

## Sample Output

```
=== Query 1: Node Degrees (Connectivity) ===
("Degree of" "Genomics" ":" 3)
("Degree of" "Assembly_VGP0" ":" 6)
("Degree of" "minimap2" ":" 4)
("Degree of" "hifiasm" ":" 4)

=== Query 2: Local Clustering Coefficient ===
("LCC of" "Genomics" ":" 0.6666666666666666)
("LCC of" "Assembly_VGP0" ":" 0.4)
("LCC of" "minimap2" ":" 0.3333333333333333)

=== Query 3a: Triangles (Closed Triads) ===
(Triangle "Genomics" "Assembly_VGP0" "minimap2")
(Triangle "Genomics" "Assembly_VGP0" "hifiasm")

=== Query 4: Hub Detection (Threshold >= 3) ===
(Hub "Genomics" (Degree 3))
(Hub "Assembly_VGP0" (Degree 6))
(Hub "minimap2" (Degree 4))
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_MORK` | `true` | Enable MORK backend |
| `CHUNK_SIZE` | `0` | Atoms per chunk (0=off) |

## References

- **MORK**: https://github.com/trueagi-io/MORK
- **MeTTa**: https://github.com/trueagi-io/hyperon-experimental
- **MM2 Format**: https://github.com/trueagi-io/MORK/wiki/Data-in-MORK

## License

Same as parent project.
