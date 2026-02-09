;; ==========================================
;; Galaxy Sample Data
;; ==========================================

;; --- NODES ---
!(add-atom &mork (: "Genomics" Category))
!(add-atom &mork (: "Assembly_VGP0" Workflow))

!(add-atom &mork (: "S1_Load" Step))
!(add-atom &mork (: "S2_Map" Step))
!(add-atom &mork (: "S3_Assemble" Step))

!(add-atom &mork (: "minimap2" Tool))
!(add-atom &mork (: "hifiasm" Tool))

!(add-atom &mork (: "fastq_reads" ToolInput))
!(add-atom &mork (: "assembly_gfa" ToolOutput))

!(add-atom &mork (: "raw_reads" Input))
!(add-atom &mork (: "mapped_reads" Output))

;; --- EDGES ---

;; 1. Hierarchy & Workflow Containment
!(add-atom &mork (HAS_WORKFLOW "Genomics" "Assembly_VGP0"))
!(add-atom &mork (HAS_TOOL "Genomics" "minimap2"))
!(add-atom &mork (HAS_TOOL "Genomics" "hifiasm"))

!(add-atom &mork (HAS_STEP "Assembly_VGP0" "S1_Load"))
!(add-atom &mork (HAS_STEP "Assembly_VGP0" "S2_Map"))
!(add-atom &mork (HAS_STEP "Assembly_VGP0" "S3_Assemble"))
!(add-atom &mork (WORKFLOW_USES_TOOL "Assembly_VGP0" "minimap2"))
!(add-atom &mork (WORKFLOW_USES_TOOL "Assembly_VGP0" "hifiasm"))

;; 2. The Chain (Flow)
!(add-atom &mork (FEEDS_INTO "S1_Load" "S2_Map"))
!(add-atom &mork (FEEDS_INTO "S2_Map" "S3_Assemble"))

;; 3. Step Details
!(add-atom &mork (STEP_USES_TOOL "S2_Map" "minimap2"))
!(add-atom &mork (STEP_USES_TOOL "S3_Assemble" "hifiasm"))
!(add-atom &mork (STEP_REQUIRES "S2_Map" "raw_reads"))
!(add-atom &mork (STEP_GENERATES "S2_Map" "mapped_reads"))

;; 4. Tool Details
!(add-atom &mork (TOOL_HAS_INPUT "minimap2" "fastq_reads"))
!(add-atom &mork (TOOL_HAS_OUTPUT "hifiasm" "assembly_gfa"))