# northstar

一个 Claude Code plugin marketplace。**README 是唯一的、无时间的目标态真理；测试是其可执行投影；历史可追溯不可权威。**

AI 的瓶颈已从"实现"上移到"设计 + 测试完善"。本框架把火力全部砸在一件事上：**把需求者意图在 README 里声明完整**——设计与测试两个瓶颈由此坍缩为同一件事。实现交给规模自适应的执行形态；代码质量类工序留给工作流，不进本 plugin。

## 安装

```bash
/plugin marketplace add TODO-你的账号/northstar
/plugin install northstar@northstar
```

安装后四个 skill 以命名空间出现：`northstar:architect` / `:module` / `:audit` / `:implement`。

## 结构

```
northstar/
├── .claude-plugin/marketplace.json     catalog
├── plugins/northstar/
│   ├── .claude-plugin/plugin.json      清单
│   └── skills/
│       ├── architect/SKILL.md          架构层：拓扑设计 + 架构结构测试（可重入）
│       ├── module/SKILL.md             模块层：内部行为契约 + 业务意图测试（循环）
│       ├── audit/SKILL.md              独立评审：零上下文审设计产物
│       └── implement/SKILL.md          令红变绿：手段按规模自选
└── README.md
```

## 节奏

`architect` 起步 → `audit`（项目级，一次）→ 然后按模块循环 `(module → audit → implement)`。

```
architect ──▶ audit ──▶ module ──▶ audit ──▶ implement ──▶ 下一模块
 (架构层)    (审项目)   (模块层)   (审模块)   (令红变绿)        │
    ▲           │         ▲          │                       │
    │ 边界错/不完整        │ 不完整/契约缺陷                   │ 测试错=契约缺陷
    └───── 回踢 ◀─────────┴────────── 回踢 ◀──────────────────┘
```

全模块完成 → **architect 收口确认架构结构测试全绿 = 项目级退出门**（补上 loop 原先缺失的项目终点）。

**回路收敛阀**：任一回边（architect 重入 / module 回踢 / implement 回踢测试）对**同一缺口**反复触发达阈值（默认 3 次，对齐 CLAUDE.md §33a）仍不收敛 → BLOCKED，停自动回踢、升级给人决策，并附该缺口的回踢历史（前几次各是什么缺口、怎么改的；过程态，进 git/Linear，不入契约）。

## 四个 skill

| skill | 层 | 职责 | 产物 | 测试 |
|---|---|---|---|---|
| `architect` | 架构·可重入 | 新项目设计拓扑 / 已有项目蒸馏 + 询问调整 | 项目 README（模块清单 + 依赖拓扑[每条边携带接口契约] + 边界接口，**不写内部**） | 架构结构测试（模块作为单元存在 + 声明公共接口可见，**纯结构·工具无关**；不验真实依赖图——边语义已由接缝契约覆盖） |
| `module` | 模块·循环 | 设计模块内部行为契约 + 派生测试 | 模块 README（**只内部**） | 业务意图行为测试（**纯行为**） |
| `audit` | 评审·独立 | **零上下文（硬性，必派子代理）**审设计产物 | 通过 / 缺口清单（门控交棒） | 审：完整度 · 契约↔测试一致 · 边界卫生 · 内部一致 |
| `implement` | 实现·规模自适应 | 令红变绿（inline / subagent / team / workflow 按规模选） | 实现代码 | 模块级退出门自出"契约合规"一刀 |

## 设计公理

- **两瓶颈坍缩为一**：AI 实现已具生产力，真问题是 ①系统设计 ②测试完善；二者皆等价于"在 README 声明完整意图"。skill 火力全砸于此。
- **时间语义分层**：目标态（README + 测试，有界，唯一真理）vs 过程态（git log / Linear / 记忆工具，单调增，可追溯不可权威）。
- **目标态拆两属性**：无时态（描述当前应有状态，非变更日志，**保留**）≠ 无历史（销毁决策理由，**拒绝**）。理由是过程态，路由出境而非删除；承重约束在热文档留**一 token 标记**（`[承重·勿删]`），理由本身交工作流（记忆/issue）。
- **两层零重叠**：架构层管拓扑（模块集 + 模块间依赖连线，纯结构），模块层管行为（给定输入、输出符合意图，纯行为）。分界点 = 模块边界本身。同一信息出现在两层 = 漂移的种子。
- **接缝闭合**：拓扑每条边携带接口契约 I；I 在架构层声明一次，上游输出测试与下游输入测试都针对同一 I → 语义兼容双向锁住，**无需独立集成层**。架构结构测试只验"模块存在 + 接口可见"，**不验真实依赖图、不验运行时接线**（A 真调用 B ≠ 各自对 stub 兼容）；后者属集成层，YAGNI 默认不做，真在意时由 README 显式声明系统级意图、落成集成性行为测试——不声明的就不测，要测先在 README 声明。
- **两级退出门**：模块级 = implement 契约合规门（实现恰好 = 模块契约）；项目级 = architect 收口门（架构结构测试全绿 = loop 终态）。状态机两级终点对称。
- **回路收敛阀**：任一回边对同一缺口反复回踢达阈值（默认 3 次，对齐 CLAUDE.md §33a）仍不收敛 → BLOCKED 升级给人，附回踢历史（过程态出境），不无限回踢。
- **测试范围铁律**：以 README 声明的意图为准。实现细节默认**不测**（实现自由发挥）；唯当 README 显式把某实现约束升格为需求，才测它。判据不是"这算不算实现"，而是"README 声明了没有"。
- **防作弊门（implement 不变量）**：测试与评审对执行循环只读——不得篡改、预判、软化；测试错则回踢上游，不在循环内静默打补丁。

## plugin 边界：纯教条，工具无关（audit 用一个平台原语）

本 plugin = 四个 skill，**教条工具无关、可分发**。唯一的平台依赖：`audit` 必须派**零上下文子代理**执行（平台原生能力，但仍是依赖——同 session 当前 agent 记得设计对话，无法真零上下文）；环境无法派子代理时 audit 不可执行，BLOCKED 升级给人，不得降级自审。除此之外，以下一律**不进 plugin**，是使用者个人全局 CLAUDE.md 的工作流配置：

- **代码质量 / 精简**（与契约无关的工程卫生）：绑 code-simplifier、code-review 等，接进 implement 之后的收尾步骤。
- **过程态路由**（决策理由、待办、历史去哪）：绑记忆工具 / Linear / git。skill 只声明"过程态不入契约、路由出境"，不声明去向。
- **契约合规评审**（实现是否恰好 = 契约）则相反——它是本框架 dogma，由 `implement` 退出门自出，不外包。

## 与 superpowers 的关系：复用，不 vendor

superpowers 是 Anthropic 官方 marketplace（`superpowers@claude-plugins-official`）分发、由 Anthropic 维护。本框架**不 pin、不接管其版本**：引擎留官方，本 plugin 只做纯自著教条层。

依据（superpowers `using-superpowers` 调度器原文）：优先级为 **用户指令（CLAUDE.md）> superpowers skill > 默认**。你的 CLAUDE.md 与本 plugin 的 skill 天然高于官方 skill，覆盖由机制保证。

### 为什么 implement 自著、不借 superpowers:test-driven-development

逐个评估契合度，**契合则借、不契合则自著**——"不造轮子"仅在"重复且无必要"时成立。superpowers TDD 有"改代码不改测试"，但**没有** northstar 独有的"测试本身错 → 回踢 architect/module 重生成"这条回路，也没有子代理模型分级；而 northstar 的"测试先于实现"已由流程顺序（README → 测试 → 实现）结构性保证，引擎核心价值对本框架冗余。故 implement 自著一薄层，只钉回路与不变量，不重造引擎。

### 已验证的机制事实（本机 6.0.3 实测）

- **skill 发现 = 纯目录约定**：`plugin.json` 不列 skill；`skills/<名>/SKILL.md` 放进去即被发现。加技能只建目录，不改清单。
- **skill 互调 = 语义相关性 + 平台 Skill 工具**，非硬路径。回路（implement 回踢 module、audit 回踢 architect）在正文点名即可，无需声明依赖。
- **版本 pin** 靠安装时记录的 `gitCommitSha`（`~/.claude/plugins/installed_plugins.json`），不在 marketplace.json 层。

> 所有 `TODO-` 占位需替换为你的真实账号/邮箱后再推 GitHub。
