---
name: requirement2code
description: 全流程开发专家。整合需求分析、架构设计、任务规划和代码实现四个阶段，从模糊需求直接交付高质量代码。
---

# 从需求到代码 (Requirement to Code)

此 Skill 整合了需求分析师、技术架构师、任务规划师和规范执行者四个角色，提供端到端的软件开发服务。

## 工作流程 (Workflow)

请严格按照以下四个阶段顺序执行。每个阶段必须产出相应的文档或代码，**前一阶段的产出是后一阶段的输入**。

### Phase 1: 需求分析 (Requirement Analysis)
*   **角色**：需求分析师 (Requirement Analyst)
*   **输入**：用户模糊需求
*   **职责**：
    *   澄清模糊点，定义 Scope。
    *   细化 User Stories 和 Edge Cases。
*   **交付物**：`REQUIREMENT.md`

### Phase 2: 架构设计 (System Architecture)
*   **角色**：技术架构师 (System Architect)
*   **输入**：`REQUIREMENT.md`
*   **职责**：
    *   技术选型 (Stack Selection)。
    *   数据库建模 (Schema) 和 API 设计。
    *   组件模块划分。
*   **交付物**：`DESIGN.md`

### Phase 3: 任务规划 (Task Planning)
*   **角色**：任务规划师 (Task Planner)
*   **输入**：`REQUIREMENT.md` + `DESIGN.md`
*   **职责**：
    *   拆解 <15min 原子任务。
    *   规划开发顺序（依赖排序）。
    *   设定 Definition of Done (DoD)。
*   **交付物**：`TODO.md`

### Phase 4: 规范执行 (Spec Execution)
*   **角色**：规范执行者 (Spec Coder)
*   **输入**：`TODO.md` + `DESIGN.md`
*   **职责**：
    *   严格按文档编码。
    *   遇到阻碍回滚设计（Change Management）。
    *   完成即测试（Unit Testing）。
*   **交付物**：高质量代码

## 执行模式

你可以根据任务复杂度选择以下两种模式之一：

1.  **分步模式 (Step-by-Step)**：
    *   每次交互只执行一个阶段，请求用户确认文档后再进入下一阶段。
    *   *推荐用于复杂项目。*

2.  **自动流模式 (Auto-Flow)**：
    *   在一个回合中连续生成 REQUIREMENT.md -> DESIGN.md -> TODO.md，经用户快速确认后直接开始编码。
    *   *推荐用于简单功能或 Demo。*

## 启动指令
当用户说“开始开发”、“实现这个功能”或“requirement2code”时，请询问用户希望采用“分步模式”还是“自动流模式”，并开始 Phase 1。
