;; Entity Types
(: Tool Type)
(: Workflow Type)
(: Community Type)

;; tool to workflow connection
(: used-in (-> Tool Workflow Experssion))

;; community assignment 
(: member-of (-> Atom Community Expression))

;; utility types
(: size (-> Workflow Number))
(: degree (-> Tool Number))
