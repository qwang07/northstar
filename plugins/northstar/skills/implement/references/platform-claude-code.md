# Claude Code 平台执行说明（绑定层）

northstar 教条正文只用抽象动作；本文声明 Claude Code 平台对 **I-平台能力表** 的逐项兑现，并承接教条抽离的平台执行细节。Codex 平台的对应说明随其绑定层轮次落地（`platform-codex.md`，待建）。

## I-平台能力表逐项兑现

| # | 能力 | Claude Code 兑现 |
|---|---|---|
| 1 | 零上下文子代理（两把刀） | audit → `ns-auditor`；code-review → `ns-reviewer`。以 Task 工具派发；dispatch 输入只含 README + 测试 / 清单（或 diff），禁背景偷渡 |
| 2 | 执行者与归因者 | implement 整模块 → `ns-implementer`；diagnose → `ns-diagnostician` |
| 3 | 只读检索 | `ns-scout` |
| 4 | 收尾精简 | `ns-simplifier` |
| 5 | 模型 / 档位分级 | 钉死于各 agent 定义 frontmatter：判断类 opus（ns-auditor / ns-reviewer / ns-diagnostician / ns-simplifier）、执行类 sonnet（ns-implementer）、检索类 haiku（ns-scout） |

## 执行三形态的平台兑现（implement 相）

- 会话内直改 → 主会话直接编辑（inline）
- 派发单执行者 → Task 工具派发 subagent
- 多执行者并行编排 → Workflow 工具编排（脚本化 fan-out），worktree 隔离防冲突

## 派发细则（教条抽离承接）

- **模型不覆写**：派发 ns-* 时不显式传 model 参数——档位已由 frontmatter 钉死；禁设 `CLAUDE_CODE_SUBAGENT_MODEL` 环境变量（其优先级高于 frontmatter，会静默架空整张路由表）。
- **未钉档的临时派发**（如天真代理压测）沿用同一分级原则选档：判断 / 评审类最高档、执行类中档、机械转录与检索类最低档——不显式指定会静默继承主会话（最贵）模型。
- **平台前置**：无；northstar 插件装上即含六 agent。
