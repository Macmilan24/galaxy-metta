
! (import! &self utils)
! (import! &self knowledge_base)

! (println! "--- Initializing Communities ---")

! (match &self (used-in (Tool $t) $w)
    (add-atom &self (member-of (Tool $t) (Community $t)))
)

;; 3. DEBUG: Verify atoms were added
! (println! "--- Debug: Checking a sample member-of atom ---")
! (match &self (member-of (Tool picard_MarkDuplicates) $c)
    (println! (format-args "CONFIRMED: picard_MarkDuplicates is in {}" ($c)))
)

;; get neighbor communities
(= (get-neighbor-comms $space $me)
   (collapse 
      (match $space 
         (used-in (Tool $me) (Workflow $w)) 
         (match $space 
            (used-in (Tool $other) (Workflow $w)) ;; Find other tools
            (match $space
                (member-of (Tool $other) (Community $c)) ;; Get their community
                $c
            )
         )
      )
   )
)

! (println! "--- Running Label Propagation ---")

! (match &self (member-of (Tool $t) (Community $c))
    (let $neighbors (get-neighbor-comms &self $t)
         (Influence $t $neighbors)
    )
)