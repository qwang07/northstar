# Codex 平台执行说明（绑定层）

northstar 教条正文只用抽象动作；本文声明 Codex CLI 平台对 **I-平台能力表** 的逐项兑现，并承接教条抽离的平台执行细节。Claude Code 平台见同目录 `platform-claude-code.md`。

## 平台前置（必须）

1. 在 `~/.codex/config.toml` 开启多代理特性，否则子代理派发不可用、audit / code-review 两把零上下文刀触发 BLOCKED：

   ```toml
   [features]
   multi_agent = true
   ```

2. 按安装指引把随仓的 agents TOML 拷入 `~/.codex/agents/`（一次性）。

## I-平台能力表逐项兑现

| # | 能力 | Codex 兑现 |
|---|---|---|
| 1 | 零上下文子代理（两把刀） | audit → `ns-auditor`；code-review → `ns-reviewer`。以显式委派提示派发（spawn_agent），委派输入只含 README + 测试 / 清单（或 diff），禁背景偷渡 |
| 2 | 执行者与归因者 | implement 整模块 → `ns-implementer`；diagnose → `ns-diagnostician` |
| 3 | 只读检索 | `ns-scout` |
| 4 | 收尾精简 | `ns-simplifier` |
| 5 | 模型 / 档位分级 | 钉死于各 agent TOML：判断类 `gpt-5.5` + high（ns-auditor / ns-reviewer / ns-diagnostician / ns-simplifier）、执行类 `gpt-5.6-terra` + medium（ns-implementer）、检索类 `gpt-5.4-mini` + low（ns-scout）；所钉集与账号型适配见安装指引 |

## 执行三形态的平台兑现（implement 相）

- 会话内直改 → 主会话直接编辑
- 派发单执行者 → 显式委派提示 spawn 一个 agent（spawn_agent / wait_agent / close_agent），执行完毕即 close
- 多执行者并行编排 → 一次委派提示 spawn 多个 agent 并行（并发上限在 `~/.codex/config.toml` 的 `[agents]` 段 `max_threads` 配置，默认 6）；以 `git worktree` 隔离防冲突——平台无内建隔离原语，委派前逐任务手工建 worktree（如 `git worktree add ../task-a -b task-a`）并在委派中指定其为工作目录，任务收编后 `git worktree remove` 清理

## 派发细则（教条抽离承接）

- **深度约束**：`agents.max_depth` 默认 1——子代理不能再派子代理；northstar 回路编排恒为"主会话 → 一层子代理"，天然兼容，勿调高该值。
- **模型不覆写**：档位已钉死于各 agent TOML；委派时不要求平台改用其他型号。
- **型号可用性**：所钉型号（gpt-5.5 / gpt-5.6-terra / gpt-5.4-mini，以安装指引型号表为准）随 OpenAI 谱系迭代，用户可在本地 `~/.codex/agents/` 副本自行改型号 / 降档；发版流程含"校验所钉型号仍有效"。
