# Codex 平台执行说明（绑定层）

northstar 教条正文只用抽象动作与声明式约束；本文是 Codex CLI 侧**唯一**的绑定载体：声明 I-平台能力表的逐项兑现、把教条声明翻译为本平台调用参数、承接教条抽离的平台执行细节。Claude Code 平台见同目录 `platform-claude-code.md`。

**不设 agent 定义文件**：执行者人格由派发者按对应 SKILL.md 现场组装（教条是唯一来源）。委派时以调用参数直接指定型号与档位，无需 `~/.codex/agents/` 下的预置定义。

## 平台前置（必须）

在 `~/.codex/config.toml` 开启多代理特性，否则委派不可用、三处硬性子代理环节触发 BLOCKED：

```toml
[features]
multi_agent = true
```

## I-平台能力表逐项兑现

| # | 能力 | Codex 兑现 |
|---|---|---|
| 1 | 零上下文子代理（audit / code-review 两把刀） | `spawn_agent` 委派，**`fork_turns: "none"`**——不继承主会话对话轮次，零上下文由此在平台层成立；`message` 内只放 README + 测试 / 清单 + 本轮 diff，禁背景偷渡 |
| 2 | 执行者（implement）与归因者（diagnose） | 同一委派路径，档位按声明取（下表） |
| 3 | 只读检索定位 | 同一委派路径，检索类低档；属横切能力，任何相可用 |
| 4 | 零写码记忆的精简执行者（simplify） | 同一委派路径，判断类高档；**工作区可写**（本相动手改，为委派默认），不叙述实施过程 |
| 5 | 模型 / 推理档位分级 | 以委派的 `model` + `reasoning_effort` 参数落定，见下表 |
| 6 | 声明式约束的翻译 | 见下两节 |

## 声明式约束 → 调用参数

`spawn_agent` 参数：`task_name`（必填，本轮任务的短标识）· `message`（必填，人格与任务全文，按对应 SKILL.md 现场组装）· `agent_type`（**本 plugin 不指定，取平台默认**；取值域未实测，无须为 northstar 用途填写）· `fork_turns` · `model` · `reasoning_effort`（实测 2026-08；注意是 `reasoning_effort`，不是配置文件里的 `model_reasoning_effort`）。下表右列取值直接作为参数值传入。

| 教条声明 | 本平台调用参数 |
|---|---|
| 推理档位 = 判断类高档 | `model: gpt-5.6-sol` + `reasoning_effort: high` |
| 推理档位 = 执行类中档 | `model: gpt-5.6-terra` + `reasoning_effort: medium` |
| 推理档位 = 检索类低档 | `model: gpt-5.6-luna` + `reasoning_effort: low` |
| 零上下文（audit / code-review） | `fork_turns: "none"` |
| 工具面 = 读写 | 默认，无需额外参数 |
| 工具面 = 只读 | **本平台无对应调用参数**——以 `message` 明令 + 返回后基线比对兑现，见下节 |

**工具面不可在委派时限制（实测 2026-08）**：上表六个参数即 `spawn_agent` 的全部，其中**没有沙箱字段**；沙箱口径由会话侧决定，委派不接受逐次覆盖。故本平台与另一平台在此同口径——只读不靠事前拦截，靠事后核验。

**`fork_turns` 约束（实测）**：使用 `model` / `reasoning_effort` 覆盖项时，`fork_turns` 必须为 `"none"` 或正整数字符串，不能是 `"all"`。零上下文两把刀恒取 `"none"`——平台约束与教条要求在此同向，不冲突。

**型号可用性**：所钉型号随 OpenAI 谱系与订阅档位而变（需 Plus 及以上；免费档降档表见安装指引）。分级原则（判断高 / 执行中 / 检索低）不变，具体型号可按订阅调整；发版流程含"校验所钉型号仍有效"。

## 只读工具面的兑现与核验（承接 README「跨平台拓扑·横切约束」）

**实测依据（2026-08）**：`spawn_agent` 不接受沙箱 / 工具面参数（全部参数见上节），事前枚举不可得，只读以**事后核验**成立：

1. **委派前记基线**：`git status --porcelain`（含未跟踪）+ `git rev-parse HEAD`。
2. **`message` 内明令**：只读——不得编辑 / 写入 / 移动任何文件，不得动工作树、暂存区与 HEAD；要看其他版本另开 worktree。**需要落草稿、日志或中间产物，写到仓库之外的临时目录**，不得落进工作树。
3. **返回后比对**：重取同一组基线值，按下述口径判定；越权 → **该次判决作废 + 回滚 + BLOCKED 升级给人**，其结论一律不采信。

**判定口径（严格）**：两次取值**完全一致**才算通过——`git status --porcelain` 输出逐字相同、`git rev-parse HEAD` 相同。任何差异都算越权，**未跟踪新增一并计入**（临时日志、缓存、草稿不豁免）。**不设白名单**：白名单一开，它自己就成了下一个后门；评审者的中间产物该落仓外，这是第 2 步明令的义务，不是核验口径该让步的地方。

**回滚按差异类型取**：有已跟踪修改 → `git checkout -- .`；有未跟踪新增 → `git clean -fd`；两者皆有则两条都跑。HEAD 变了 → 属改动历史，不自行回滚，直接 BLOCKED 升级给人。

比对不通过属"独立性已破"，不是"小问题"——评审者动过手，它的判决就不再是零上下文判决。

## 执行三形态的平台兑现（implement 相）

- 会话内直改 → 主会话直接编辑
- 派发单执行者 → 一次委派 spawn 一个 agent（`spawn_agent` / `wait_agent` / `close_agent`），执行完毕即 close
- 多执行者并行编排 → 一次委派 spawn 多个 agent 并行（并发上限在 `~/.codex/config.toml` 的 `[agents]` 段 `max_threads`，默认 6）；以 `git worktree` 隔离防冲突——平台无内建隔离原语，委派前逐任务手工建 worktree（如 `git worktree add ../task-a -b task-a`），收编后 `git worktree remove` 清理。**工作目录同样无对应调用参数**（六参数里没有 cwd / workdir 字段），比照只读的办法兑现：在 `message` 内以**绝对路径明令**该执行者只在其 worktree 内作业，不得触及主工作树或他人 worktree

## 派发细则（教条抽离承接）

- **人格现场组装**：委派 `message` 按对应 SKILL.md 现写，不另存副本。教条改了，下一次委派自动跟上——这是删除 agent TOML 换来的单源性，也免去了"改仓库后须重拷 TOML"的手工同步。
- **深度约束**：`agents.max_depth` 默认 1——子代理不能再派子代理；northstar 回路编排恒为"主会话 → 一层子代理"，天然兼容，勿调高该值。
- **内循环 diff 核对**：主会话亲自读 diff，或轻量委派一个判断类高档评审者提前把关——收尾 code-review 刀不因此免除。
- **回合固化兑现**：教条「回合起点与固化」在本平台以 git 提交兑现——起点 = 回合入口记录的提交号（过程态出境），固化 = implement 退出前提交；「本轮 diff」即两提交之差（`git diff 起点..固化点`）。
