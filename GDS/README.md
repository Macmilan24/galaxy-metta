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

## Sample Output

```text
("checking query 1 ...")
("Degree of" "Genomics" ":" 3)
("Degree of" "Assembly_VGP0" ":" 6)
("Degree of" "minimap2" ":" 4)
("Degree of" "hifiasm" ":" 4)
("Degree of" "S1_Load" ":" 2)
("Degree of" "S2_Map" ":" 6)
("Degree of" "S3_Assemble" ":" 3)
("Degree of" "fastq_reads" ":" 1)
("Degree of" "assembly_gfa" ":" 1)
("Checking query 2: Clustering Coefficient ...")
("LCC of" "Genomics" ":" 0.6666666666666666)
("LCC of" "Assembly_VGP0" ":" 0.4)
("LCC of" "minimap2" ":" 0.3333333333333333)
("LCC of" "hifiasm" ":" 0.3333333333333333)
("LCC of" "S1_Load" ":" 1)
("LCC of" "S2_Map" ":" 0.2)
("LCC of" "S3_Assemble" ":" 0.6666666666666666)
("LCC of" "fastq_reads" ":" 0.0)
("LCC of" "assembly_gfa" ":" 0.0)
("Motif: Triangles Found:")
(Triangle "Genomics" "Assembly_VGP0" "minimap2")
(Triangle "Genomics" "Assembly_VGP0" "hifiasm")
(Triangle "Genomics" "minimap2" "Assembly_VGP0")
(Triangle "Genomics" "hifiasm" "Assembly_VGP0")
(Triangle "Assembly_VGP0" "S1_Load" "S2_Map")
(Triangle "Assembly_VGP0" "S2_Map" "S1_Load")
(Triangle "Assembly_VGP0" "S2_Map" "S3_Assemble")
(Triangle "Assembly_VGP0" "S2_Map" "minimap2")
(Triangle "Assembly_VGP0" "S3_Assemble" "S2_Map")
(Triangle "Assembly_VGP0" "S3_Assemble" "hifiasm")
(Triangle "Assembly_VGP0" "minimap2" "S2_Map")
(Triangle "Assembly_VGP0" "minimap2" "Genomics")
(Triangle "Assembly_VGP0" "hifiasm" "S3_Assemble")
(Triangle "Assembly_VGP0" "hifiasm" "Genomics")
(Triangle "Assembly_VGP0" "Genomics" "minimap2")
(Triangle "Assembly_VGP0" "Genomics" "hifiasm")
(Triangle "minimap2" "Genomics" "Assembly_VGP0")
(Triangle "minimap2" "Assembly_VGP0" "Genomics")
(Triangle "minimap2" "Assembly_VGP0" "S2_Map")
(Triangle "minimap2" "S2_Map" "Assembly_VGP0")
(Triangle "hifiasm" "Genomics" "Assembly_VGP0")
(Triangle "hifiasm" "Assembly_VGP0" "Genomics")
(Triangle "hifiasm" "Assembly_VGP0" "S3_Assemble")
(Triangle "hifiasm" "S3_Assemble" "Assembly_VGP0")
(Triangle "S1_Load" "S2_Map" "Assembly_VGP0")
(Triangle "S1_Load" "Assembly_VGP0" "S2_Map")
(Triangle "S2_Map" "S3_Assemble" "Assembly_VGP0")
(Triangle "S2_Map" "minimap2" "Assembly_VGP0")
(Triangle "S2_Map" "Assembly_VGP0" "S3_Assemble")
(Triangle "S2_Map" "Assembly_VGP0" "minimap2")
(Triangle "S2_Map" "Assembly_VGP0" "S1_Load")
(Triangle "S2_Map" "S1_Load" "Assembly_VGP0")
(Triangle "S3_Assemble" "hifiasm" "Assembly_VGP0")
(Triangle "S3_Assemble" "Assembly_VGP0" "hifiasm")
(Triangle "S3_Assemble" "Assembly_VGP0" "S2_Map")
(Triangle "S3_Assemble" "S2_Map" "Assembly_VGP0")
("Motif: Open Triads Found:")
(OpenTriad "Genomics" "->" "Assembly_VGP0" "->" "S1_Load")
(OpenTriad "Genomics" "->" "Assembly_VGP0" "->" "S2_Map")
(OpenTriad "Genomics" "->" "Assembly_VGP0" "->" "S3_Assemble")
(OpenTriad "Genomics" "->" "minimap2" "->" "fastq_reads")
(OpenTriad "Genomics" "->" "minimap2" "->" "S2_Map")
(OpenTriad "Genomics" "->" "hifiasm" "->" "assembly_gfa")
(OpenTriad "Genomics" "->" "hifiasm" "->" "S3_Assemble")
(OpenTriad "Assembly_VGP0" "->" "S2_Map" "->" "mapped_reads")
(OpenTriad "Assembly_VGP0" "->" "S2_Map" "->" "raw_reads")
(OpenTriad "Assembly_VGP0" "->" "minimap2" "->" "fastq_reads")
(OpenTriad "Assembly_VGP0" "->" "hifiasm" "->" "assembly_gfa")
(OpenTriad "minimap2" "->" "Genomics" "->" "hifiasm")
(OpenTriad "minimap2" "->" "Assembly_VGP0" "->" "S1_Load")
(OpenTriad "minimap2" "->" "Assembly_VGP0" "->" "S3_Assemble")
(OpenTriad "minimap2" "->" "Assembly_VGP0" "->" "hifiasm")
(OpenTriad "minimap2" "->" "S2_Map" "->" "S3_Assemble")
(OpenTriad "minimap2" "->" "S2_Map" "->" "mapped_reads")
(OpenTriad "minimap2" "->" "S2_Map" "->" "raw_reads")
(OpenTriad "minimap2" "->" "S2_Map" "->" "S1_Load")
(OpenTriad "hifiasm" "->" "Genomics" "->" "minimap2")
(OpenTriad "hifiasm" "->" "Assembly_VGP0" "->" "S1_Load")
(OpenTriad "hifiasm" "->" "Assembly_VGP0" "->" "S2_Map")
(OpenTriad "hifiasm" "->" "Assembly_VGP0" "->" "minimap2")
(OpenTriad "hifiasm" "->" "S3_Assemble" "->" "S2_Map")
(OpenTriad "S1_Load" "->" "S2_Map" "->" "S3_Assemble")
(OpenTriad "S1_Load" "->" "S2_Map" "->" "minimap2")
(OpenTriad "S1_Load" "->" "S2_Map" "->" "mapped_reads")
(OpenTriad "S1_Load" "->" "S2_Map" "->" "raw_reads")
(OpenTriad "S1_Load" "->" "Assembly_VGP0" "->" "S3_Assemble")
(OpenTriad "S1_Load" "->" "Assembly_VGP0" "->" "minimap2")
(OpenTriad "S1_Load" "->" "Assembly_VGP0" "->" "hifiasm")
(OpenTriad "S1_Load" "->" "Assembly_VGP0" "->" "Genomics")
(OpenTriad "S2_Map" "->" "S3_Assemble" "->" "hifiasm")
(OpenTriad "S2_Map" "->" "minimap2" "->" "fastq_reads")
(OpenTriad "S2_Map" "->" "minimap2" "->" "Genomics")
(OpenTriad "S2_Map" "->" "Assembly_VGP0" "->" "hifiasm")
(OpenTriad "S2_Map" "->" "Assembly_VGP0" "->" "Genomics")
(OpenTriad "S3_Assemble" "->" "hifiasm" "->" "assembly_gfa")
(OpenTriad "S3_Assemble" "->" "hifiasm" "->" "Genomics")
(OpenTriad "S3_Assemble" "->" "Assembly_VGP0" "->" "S1_Load")
(OpenTriad "S3_Assemble" "->" "Assembly_VGP0" "->" "minimap2")
(OpenTriad "S3_Assemble" "->" "Assembly_VGP0" "->" "Genomics")
(OpenTriad "S3_Assemble" "->" "S2_Map" "->" "minimap2")
(OpenTriad "S3_Assemble" "->" "S2_Map" "->" "mapped_reads")
(OpenTriad "S3_Assemble" "->" "S2_Map" "->" "raw_reads")
(OpenTriad "S3_Assemble" "->" "S2_Map" "->" "S1_Load")
(OpenTriad "fastq_reads" "->" "minimap2" "->" "Genomics")
(OpenTriad "fastq_reads" "->" "minimap2" "->" "Assembly_VGP0")
(OpenTriad "fastq_reads" "->" "minimap2" "->" "S2_Map")
(OpenTriad "assembly_gfa" "->" "hifiasm" "->" "Genomics")
(OpenTriad "assembly_gfa" "->" "hifiasm" "->" "Assembly_VGP0")
(OpenTriad "assembly_gfa" "->" "hifiasm" "->" "S3_Assemble")
("Checking Hubs (Threshold >= 3):")
(Hub "Genomics" (Degree 3))
(Hub "Assembly_VGP0" (Degree 6))
(Hub "minimap2" (Degree 4))
(Hub "hifiasm" (Degree 4))
(Hub "S2_Map" (Degree 6))
(Hub "S3_Assemble" (Degree 3))
```
