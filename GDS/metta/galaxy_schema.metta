;; Nodes Types

!(add-atom &mork (: Category Type))
!(add-atom &mork (: Workflow Type))
!(add-atom &mork (: Step Type))
!(add-atom &mork (: Tool Type))
!(add-atom &mork (: ToolInput Type))
!(add-atom &mork (: ToolOutput Type))
!(add-atom &mork (: Input Type))
!(add-atom &mork (: Output Type))

;; Relationship types
!(add-atom &mork (: HAS_WORKFLOW (-> Category Workflow Type)))
!(add-atom &mork (: HAS_STEP (-> Workflow Step Type)))
!(add-atom &mork (: FEEDS_INTO (-> Step Step Type)))
!(add-atom &mork (: STEP_USES_TOOL (-> Step Tool Type)))

!(add-atom &mork (: TOOL_HAS_INPUT (-> Tool ToolInput Type)))
!(add-atom &mork (: TOOL_HAS_OUTPUT (-> Tool ToolOutput Type)))

!(add-atom &mork (: STEP_GENERATES (-> Step Output Type)))
!(add-atom &mork (: STEP_REQUIRES (-> Step Input Type)))
!(add-atom &mork (: WORKFLOW_USES_TOOL (-> Workflow Tool Type)))