;; Recursive List length function

(: len (-> Experssion Number))
(= (len () ) 0)
(= (len ($x $xs)) (+ 1 (len $xs)))

(= (count $pattern)
    (len (collapse $pattern))
)