!(import! &self types)
!(import! &self utils)
!(import! &self knowledge_base)

;; calculate Hyperdegree (k) of a Tool

(= (get-hyperdegree $space $t)
   (count (match $space (used-in (Tool $t) $w) $w))
)
;; calculate Cardinality (m) of a workflow
;; how many tools are in this workflow

(= (get-cardinality $space $w)
   (count (match $space (used-in $t (Workflow $w)) $t))
)

!(println! "--- Analyzing Graph Topology ---")

!(match &self
    (used-in (Tool $t) (Workflow $w))
    (let*
        (
            ($k (get-hyperdegree &self $t))
            ($m (get-cardinality &self $w))
        )

        (Analyzing (Tool $t has-degree $k) (Workflow $w has-size $m))
    )
)