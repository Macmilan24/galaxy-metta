;; ==========================================
;; Galaxy Sample Data
;; ==========================================

;; --- NODES ---
(: "Genomics" Category)
(: "Assembly_VGP0" Workflow)

(: "S1_Load" Step)
(: "S2_Map" Step)
(: "S3_Assemble" Step)

(: "minimap2" Tool)
(: "hifiasm" Tool)

(: "fastq_reads" ToolInput)
(: "assembly_gfa" ToolOutput)

(: "raw_reads" Input)
(: "mapped_reads" Output)

;; --- EDGES ---

;; 1. Hierarchy & Workflow Containment
(HAS_WORKFLOW "Genomics" "Assembly_VGP0")
(HAS_TOOL "Genomics" "minimap2")
(HAS_TOOL "Genomics" "hifiasm")

(HAS_STEP "Assembly_VGP0" "S1_Load")
(HAS_STEP "Assembly_VGP0" "S2_Map")
(HAS_STEP "Assembly_VGP0" "S3_Assemble")
(WORKFLOW_USES_TOOL "Assembly_VGP0" "minimap2")
(WORKFLOW_USES_TOOL "Assembly_VGP0" "hifiasm")

;; 2. The Chain (Flow)
(FEEDS_INTO "S1_Load" "S2_Map")
(FEEDS_INTO "S2_Map" "S3_Assemble")

;; 3. Step Details
(STEP_USES_TOOL "S2_Map" "minimap2")
(STEP_USES_TOOL "S3_Assemble" "hifiasm")
(STEP_REQUIRES "S2_Map" "raw_reads")
(STEP_GENERATES "S2_Map" "mapped_reads")

;; 4. Tool Details
(TOOL_HAS_INPUT "minimap2" "fastq_reads")
(TOOL_HAS_OUTPUT "hifiasm" "assembly_gfa")