;; Query 1: Connectivity and degree

;; helper for counting
(= (count-plus-one $atom $acc) (+ 1 $acc))

;; define what is an edge
(= (gds-edge) HAS_WORKFLOW)
(= (gds-edge) HAS_TOOL)
(= (gds-edge) HAS_STEP)
(= (gds-edge) WORKFLOW_USES_TOOL)
(= (gds-edge) FEEDS_INTO)
(= (gds-edge) STEP_USES_TOOL)
(= (gds-edge) STEP_GENERATES)
(= (gds-edge) STEP_REQUIRES)
(= (gds-edge) TOOL_HAS_INPUT)
(= (gds-edge) TOOL_HAS_OUTPUT)


;; Match relation node to y or  y to node
(= (neighbors-of $node)
   (let $pred (gds-edge)
      (match &self ($pred $node $y) $y)
   )
)

(= (neighbors-of $node)
   (let $pred (gds-edge)
      (match &self ($pred $y $node) $y)
   )
)

;; sum all neighbors
(= (get-degree $node)
   (foldall count-plus-one (neighbors-of $node) 0)
)

;; =====================================
;; Query Excusions
;; =====================================
!("checking query 1 ...")
!("Degree of minimap2:" (get-degree "minimap2"))


;;==================================
;; Query 2 Triadic closure
;;==================================

;; helper check if connected
(= (check-connection $x $y)
   (let $pred (gds-edge)
      (match &self ($pred $x $y) True)
   )
)

(= (check-connection $x $y)
   (let $pred (gds-edge)
      (match &self ($pred $y $x) True)
   )
)

;; count triangle for a node
(= (triangle-count $node)
   (foldall count-plus-one
      (let $b (neighbors-of $node)
         (let $c (neighbors-of $node)
            (if (and
               (not (== $b $c))
               (check-connection $b $c)
            )
            (FoundTriangle)
            (empty)
            )
         )
      )
      0
   )
)

;; calculate possible triangles
(= (possible-triangles $k)
   (* $k (- $k 1))
)

;; function to get clustering coefficient
(= (get-lcc $node)
   (let $k (get-degree $node)
      (if (< $k 2)
         0.0
         (let $tri-pairs (triangle-count $node)
            (/ $tri-pairs (possible-triangles $k))
         )
      )
   )
)

;; =====================================
;; Query Excusions
;; =====================================
!("Checking query 2: Clustering Coefficient ...")
!("LCC of Genomics:" (get-lcc "Genomics"))
!("LCC of minimap2:" (get-lcc "minimap2"))


;; ==================================
;; Query 3: Motifs & Hubs
;; ==================================

(= (get-all-nodes)
   (match &self (: $node $type) $node)
)
;; finding triangle
!("Motif: Triangles Found:")
!(let $node (get-all-nodes) 
   (let $b (neighbors-of $node)
      (let $c (neighbors-of $node)
         (if (and
            (not (== $b $c))
            (check-connection $b $c)
         )
         (Triangle $node $b $c)
         (empty)
         )
      )
   )
)  



;; helper to check no connection
(= (not-connected $x $y)
   (== (collapse (check-connection $x $y)) ())
)

;; motifs open Triads
!("Motif: Open Triads Found:")
!(let $a (get-all-nodes) 
   (let $b (neighbors-of $a)
      (let $c (neighbors-of $b)
         (if (and
            (not (== $a $c))
            (not-connected $a $c)
         )
         (OpenTriad $a "->" $b "->" $c)
         (empty)
         )
      )
   )
)


;; Hub Analysis
(= (find-hubs $threshold)
   (let $node (get-all-nodes)
      (let $d (get-degree $node)
         (if (>= $d $threshold)
            (Hub $node (Degree $d))
            (empty)
         )
      )
   )
)

!("Checking Hubs (Threshold >= 3):")
!(find-hubs 3)