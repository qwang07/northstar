# northstar

简体中文 | [English](README.en.md)

一个 Claude Code plugin marketplace。**README 是唯一的、无时间的目标态真理；测试是其可执行投影；历史可追溯不可权威。**

AI 的瓶颈已从"实现"上移到"设计 + 测试完善"。本框架把火力全部砸在一件事上：**把需求者意图在 README 里声明完整**——设计与测试两个瓶颈由此坍缩为同一件事。回路按**活动**切分：契约对话（brainstorming）→ 派生守护物（write-test）→ 独立评审（audit）→ 令红变绿（implement）；缺陷经 diagnose 归因入口进入，收尾由 code-review 出质量刀。**六个 skill 与六个执行子代理全自著、零外部 plugin 依赖（不挂 superpowers 等任何引擎），装上即独立运行。**

## 安装

```bash
/plugin marketplace add qwang07/northstar
/plugin install northstar@northstar
```

安装后六个 skill 以命名空间出现：`northstar:brainstorming` / `:write-test` / `:audit` / `:implement` / `:diagnose` / `:code-review`；Claude Code 侧六个执行子代理随插件注册：`ns-scout` / `ns-diagnostician` / `ns-auditor` / `ns-implementer` / `ns-simplifier` / `ns-reviewer`。

Codex CLI 侧：skills 经同仓插件清单安装；agents 为随仓 TOML，按一次性安装指引（`docs/codex-install.md`，含实测命令与所钉型号表）拷入用户 agents 目录（条款见「跨平台拓扑」节）。

## 结构

```
northstar/
├── .claude-plugin/marketplace.json     Claude Code catalog
├── plugins/northstar/
│   ├── .claude-plugin/plugin.json      清单
│   ├── skills/
│   │   ├── brainstorming/SKILL.md      契约相：对话出 README（唯一写入口，按权威层落位）
│   │   ├── write-test/SKILL.md         测试相：从 README 派生测试或验证清单
│   │   ├── audit/SKILL.md              独立评审：零上下文审设计产物（双检查点）
│   │   ├── implement/SKILL.md          令红变绿：手段按规模自选
│   │   ├── diagnose/SKILL.md           缺陷入口：归因先于修复，出口分流回路
│   │   └── code-review/SKILL.md        收尾质量刀：零上下文审代码质量
│   └── agents/
│       ├── ns-scout.md                 只读检索（haiku）
│       ├── ns-diagnostician.md         diagnose 相归因者（opus）
│       ├── ns-auditor.md               audit 相零上下文评审者（opus）
│       ├── ns-implementer.md           implement 相模块级执行者（sonnet）
│       ├── ns-simplifier.md            收尾链精简工序（opus）
│       └── ns-reviewer.md              code-review 相零上下文评审者（opus）
├── .codex-plugin/plugin.json           Codex 插件清单（skills 字段指向上方共享教条层）
├── .agents/plugins/marketplace.json    Codex marketplace 清单
├── .codex/agents/                      Codex 绑定层：六 agent TOML（随仓分发，一次性拷入用户目录）
├── docs/codex-install.md               Codex 安装指引（实测命令 + 所钉型号表）
├── tests/structure.py                  项目级结构测试（拓扑形状 / 绑定分级 / 禁词不变量 / 引用完整性）
├── README.md
└── README.en.md
```

## 节奏

```
（缺陷）──▶ diagnose ──归因分流──▶┐
（新需求）──────────────────────▶ brainstorming ──▶ write-test ──▶ audit ──▶ 人 Gate ──▶ implement ──▶ 收尾链
                                 (契约相·README)   (测试 / 清单)  (零上下文)              (红变绿)     (simplifier→code-review)
                                    ▲     ▲             ▲                                   │
                                    │     └─ 契约缺口回踢 ┴──────── 测试缺口回踢 ◀───────────┘
                                    └────────────── 收口（项目级退出门）◀────────── 全模块完成
```

- **切分轴是活动，回合由目标定义**：契约对话 / 写测试 / 评审 / 实施各占一相。契约条款按权威层落位——项目级（拓扑与边界）/ 横切层（多模块共守约束，按需存在）/ 模块级（内部行为）；高度是落位结果，不是入口参数。
- **粒度阀**：本轮目标需展开超过一个模块的内部契约 → 本轮止于分解（产子目标清单 + 项目级 / 横切层条款），各子目标下轮逐个成轮 `brainstorming → write-test → audit → implement`。
- **免测试分支**：纯一次性操作（迁移 / 灌数 / 一次性脚本）不派生测试，由 write-test 改产**机械可判定的验证清单**，同交 audit 审；implement 以清单逐项过为完成判据。
- **audit 双检查点**：brainstorming 定稿后（跨模块目标契约先审，省派生返工）+ write-test 完成后（README + 测试 / 清单合卷）；单模块目标可并为一次合卷审。
- **收口**：全部模块完成 → 回到 brainstorming 收口——架构结构测试全绿 + 业务流走查复跑 = 项目级退出门（loop 终态）。
- **回路收敛阀**：任一回边对**同一缺口**反复触发达阈值（默认 3 次）仍不收敛 → BLOCKED，停自动回踢、升级给人决策，附该缺口回踢历史（过程态，进 git/Linear，不入契约）。

## 用法

一次只推进一个范围，对话里描述意图即触发对应 skill：

- **新项目**：`brainstorming`（跨模块目标）设计拓扑（模块清单 + 依赖 + 接口契约），经 `audit` 把关，再逐模块 `brainstorming → write-test → audit → implement`，全部完成回 `brainstorming` 收口。
- **已有项目**：`brainstorming` 先蒸馏现有结构、问你是否调整，确立目标态后同上。
- **改 bug**：红因不明 / 生产缺陷先进 `diagnose` 归因，按出口分流（实现错 → implement；契约缺口 → brainstorming；测试错 / 断言弱 → write-test）。
- **小改动**：纯实现的小改直接 `implement` 会话内直改；触及契约的，先回 `brainstorming` 改 README、`write-test` 改测试，再实现。

分工：契约与测试阶段，**人**把需求者意图逼问完整、确认契约；**skill** 把契约落成守护物、把红改绿。一句话——**契约由人定，红变绿由 AI 做。**

## 六个 skill

| skill | 相 | 职责 | 产物 |
|---|---|---|---|
| `brainstorming` | 契约·README 唯一写入口 | 目标开题、对话逼问意图完整（一次一问）；存量代码先蒸馏再问调整；定稿前业务流走查；全模块完成后收口 | 按目标落位的 README 条款：项目级（模块清单 + 拓扑[每条边携带接口契约] + 边界接口，**不写内部**）/ 横切层（多模块共守约束，按需存在）/ 模块级（职责边界 / 应有功能 / 接口契约 / 边界与不变量，**只内部**） |
| `write-test` | 测试·派生 | 裁分支（需持续守护→测试；一次性→验证清单）；测意图不测实现；强断言纪律 | 独立测试文件（初始红：业务意图测试 + 结构测试[模块存在 / 接口可见 / 持续不变量]）或机械可判定验证清单 |
| `audit` | 评审·独立 | **零上下文（硬性，必派子代理）**审设计产物；双检查点；缺口分流回踢 | 通过 / 缺口清单（门控交棒）。五审项：完整度 · 契约↔测试一致 · 边界卫生 · 内部一致 · **断言强度** |
| `implement` | 实现·规模自适应 | 完整小循环：验红→绿→验绿(回归)→重构 →契约合规门→验证（会话内直改 / 派发单执行者 / 并行编排，按规模选）；免测试分支以清单逐项过为完成判据 | 实现代码 |
| `diagnose` | 缺陷入口 | 归因先于修复；取证→模式对照→假设检验→分流 | 复现红测试（→implement）/ 契约缺口（→brainstorming）/ 修测清单（→write-test）/ 外部问题留档 |
| `code-review` | 收尾·质量刀 | 零上下文审代码质量（潜在 bug / 静默失败 / 可维护性），锚定模块 README 为规格；发现处置：复核→满足 / 回踢 / 有据驳回 | 严重度分档发现 + 明确裁决（可收尾 / 需修后收尾） |

## 设计理念（核心公理）

- **两瓶颈坍缩为一**：AI 实现已具生产力，真问题是 ①系统设计 ②测试完善；二者皆等价于"在 README 声明完整意图"。skill 火力全砸于此。
- **按活动切分，目标定回合**：契约对话、写测试、评审、实施是四种活动，各占一相；回合由目标定义（这轮达成什么、怎么算达成），项目级 / 横切层 / 模块级只是条款的落位层。同一活动不因高度拆成两个 skill——那是镜像税的温床。
- **README 唯一写入口**：全回路只有 brainstorming 可写 README；audit / write-test / implement / diagnose 对 README 只读，发现缺口回踢。配套：一处权威 + 指针，禁止跨 README 复述。
- **时间语义分层**：目标态（README + 测试，有界，唯一真理）vs 过程态（git log / Linear / 记忆工具，单调增，可追溯不可权威）。
- **目标态拆两属性**：无时态（描述当前应有状态，非变更日志，**保留**）≠ 无历史（销毁决策理由，**拒绝**）。理由是过程态，路由出境而非删除；承重约束在热文档留**一 token 标记**（`[承重·勿删]`），理由本身交工作流（记忆/issue）。
- **各层零重叠**：README 树按项目实际结构分层——项目级管拓扑（模块集 + 依赖连线，纯结构），横切层管多模块共守约束（按需存在），模块级管行为（给定输入、输出符合意图）；每条契约只在其权威层声明，下层以指针承接。同一信息出现在两层 = 漂移的种子。
- **接缝闭合**：拓扑每条边携带接口契约 I；I 在项目级声明一次，上游输出测试与下游输入测试都针对同一 I → 语义兼容双向锁住，**无需独立集成层**。结构测试只验"模块存在 + 接口可见 + 持续不变量"，**不验真实依赖图、不验运行时接线**；后者属集成层，YAGNI 默认不做，真在意时由 README 显式声明系统级意图、落成集成性行为测试——不声明的就不测，要测先在 README 声明。
- **业务流走查**：各相各管一段，没人天然负责把一条业务流从头走到尾——断链（吞错闭环、信号无消费端、悬挂状态）不会被任何单相发现。故 brainstorming 定稿与收口时把 README 契约网当状态机，正向 + 逆向 + 异常路径逐环节找承接契约。
- **强断言纪律**：测了但断言恒真 = 零判别力，比没测更危险（制造已覆盖假象）。write-test 派生时禁恒真断言 / 只断状态码 / 松匹配枚举 / 精度不锁；audit 第五审项专查断言强度。
- **两级退出门**：模块级 = implement 契约合规门（实现恰好 = 模块契约）；项目级 = brainstorming 收口门（结构测试全绿 + 业务流走查过 = loop 终态）。
- **回路收敛阀**：任一回边对同一缺口反复回踢达阈值（默认 3 次）仍不收敛 → BLOCKED 升级给人，附回踢历史（过程态出境），不无限回踢。
- **测试范围铁律**：以 README 声明的意图为准。实现细节默认**不测**（实现自由发挥）；唯当 README 显式把某实现约束升格为需求，才测它。判据不是"这算不算实现"，而是"README 声明了没有"。
- **防作弊门（implement 不变量）**：测试与评审对执行循环只读——不得篡改、预判、软化；测试错则回踢上游，不在循环内静默打补丁。
- **归因先于修复**：缺陷不经归因不得修复；"看起来像 X 就改 X"是 diagnose 要消灭的行为。修复永远发生在 implement，diagnose 只产可交接工件。

## 跨平台拓扑：教条单源，绑定双写

northstar 面向 Claude Code 与 Codex CLI 双平台分发。三层结构，层间以接口契约相连：

```
教条层    plugins/northstar/skills/ 六 SKILL.md —— 单源，平台无关
   ▲ 经 I-平台能力表
绑定层    Claude Code：plugins/northstar/agents/*.md（frontmatter 钉 opus/sonnet/haiku）
          Codex：agents TOML（遵平台 agent schema，钉具体型号 + reasoning effort 档位）
   ▲
分发层    Claude Code：.claude-plugin/ marketplace
          Codex：同仓插件清单（遵平台约定 .codex-plugin/plugin.json + marketplace 清单 .agents/plugins/marketplace.json）；agents 不入插件，随仓分发 + 一次性安装指引
```

绑定层 = agents 定义 + **平台执行说明**（每平台一份：I-平台能力表的逐项兑现声明、教条抽离的平台专属执行细节、平台前置配置，皆落于此；教条正文以指针引用，位置属实现自由）。平台专属的判据：执行形态与机制的**平台具名词**（某平台对"会话内直改 / 派发单执行者 / 多执行者并行编排"三形态及其隔离机制的具体命名与语法）属抽离对象；跨平台共有的抽象概念（子代理、派发、只读检索）保留在教条。

**I-平台能力表**（教条层↔绑定层的接口契约）：教条正文只用抽象动作表述平台行为，每个绑定层逐项声明本平台兑现方式——
1. 派发零上下文子代理（audit / code-review 两把刀）
2. 派发模块级执行者（implement）与归因者（diagnose）
3. 只读检索定位
4. 收尾精简工序
5. 模型 / 推理档位分级：判断类高档（评审 / 归因 / 精简）、执行类中档、检索类低档

**横切约束（双绑定层共守）**：
- 教条正文禁现平台专属名词（工具名 / 配置字段 / 调用语法），落成可机械断言的持续不变量
- 绑定层对 I-平台能力表逐项兑现；任一项不可兑现 = 该平台对应环节显式不可用，禁静默降级（零上下文一项承接下节 BLOCKED 公理，指针不复述）
- 回路编排恒为"主会话 → 一层子代理"，任何 skill 不得要求子代理再派子代理
- Codex 绑定钉具体型号：安装指引须声明所需型号并注明用户可在本地副本自行改型号 / 降档；发版流程含"校验所钉型号仍有效"一项 `[承重·勿删]`

## plugin 边界：教条 + 执行绑定（两把零上下文刀共用一个平台原语）

本 plugin = 六个 skill（教条，工具无关）+ 六个子代理（执行绑定：各相执行者与模型分级；Claude Code 侧随插件分发，Codex 侧为同一套定义的 TOML 随仓分发——见「跨平台拓扑」节；均入版本管理，结束游离状态）。平台依赖：`audit` 与 `code-review` 必须派**零上下文子代理**执行（平台原生能力，但仍是依赖——同 session 当前 agent 记得设计对话，无法真零上下文）；环境无法派子代理时该环节不可执行，BLOCKED 升级给人，不得降级自审。除此之外，以下一律**不进 plugin**，是使用者个人全局 CLAUDE.md 的工作流配置：

- **过程态路由**（决策理由、待办、历史去哪）：绑记忆工具 / Linear / git。skill 只声明"过程态不入契约、路由出境"，不声明去向。
- **契约合规评审**（实现是否恰好 = 契约）则相反——它是本框架 dogma，由 `implement` 退出门自出，不外包。

## 独立性：自成一体，不挂外部引擎

六个 skill 与六个子代理全自著，**不依赖、不复用、不 pin 任何外部 plugin**（含 superpowers 等官方引擎；精简工序 ns-simplifier 消化自官方 code-simplifier 后自著，来源行留于其定义文件）。northstar 装上即可独立运行。

**为什么不挂任何外部引擎**：曾考虑借现成 TDD / 评审引擎，逐个评估契合度后放弃——"不造轮子"仅在"重复且无必要"时成立，而 northstar 有外部引擎给不了的东西：

- "测试本身错 → 回踢 brainstorming / write-test 重生成"这条回路，以及子代理模型分级——通用引擎没有；
- "测试先于实现"已由流程顺序（README → 测试 → 实现）**结构性保证**，引擎的核心价值对本框架冗余。

故每个 skill 自著一薄层，只钉自己的回路与不变量，不重造引擎。已消化的外部方法论（brainstorming / write-test 的对话与派生范式、systematic-debugging → diagnose、receiving-code-review → code-review 处置节、writing-skills 的天真代理压测 → 本仓库 skill 文本的验收门）在对应 SKILL.md 末尾留来源行，可追溯不 vendor。

### Claude Code plugin 机制事实（实测）

- **skill 发现 = 纯目录约定**：`plugin.json` 不列 skill；`skills/<名>/SKILL.md` 放进去即被发现。加技能只建目录，不改清单。
- **skill 互调 = 语义相关性 + 平台 Skill 工具**，非硬路径。回路（implement 回踢 write-test、audit 回踢 brainstorming）在正文点名即可，无需声明依赖。
- **覆盖优先级 = 用户指令（CLAUDE.md）> plugin skill > 默认**：你的 CLAUDE.md 天然高于任何 plugin skill，冲突由机制保证。
- **版本 pin** 靠安装时记录的 `gitCommitSha`（`~/.claude/plugins/installed_plugins.json`），不在 marketplace.json 层。
