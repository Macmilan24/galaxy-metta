;; Nodes Types

(: Category Type)
(: Workflow Type)
(: Step Type)
(: Tool Type)
(: ToolInput Type)
(: ToolOutput Type)
(: Input Type)
(: Output Type)

;; Relationship types
(: HAS_WORKFLOW (-> Category Workflow Type))
(: HAS_STEP (-> Workflow Step Type))
(: FEEDS_INTO (-> Step Step Type))
(: STEP_USES_TOOL (-> Step Tool Type))

(: TOOL_HAS_INPUT (-> Tool ToolInput Type))
(: TOOL_HAS_OUTPUT (-> Tool ToolOutput Type))

(: STEP_GENERATES (-> Step Output Type))
(: STEP_REQUIRES (-> Step Input Type))
(: WORKFLOW_USES_TOOL (-> Workflow Tool Type))