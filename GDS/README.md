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
First, convert the raw JSON data into MeTTa format:
```bash
python3 python/json_to_metta.py
```

### 2. Run Queries
To run the analysis on the sample data (default):
```bash
./run_gds.sh
```

To run on the full dataset, ensure `galaxy_queries.metta` imports `galaxy_data_full.metta`.
