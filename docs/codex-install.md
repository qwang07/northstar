# Codex CLI 安装指引（一次性）

northstar 在 Codex 侧分两部分：skills 经插件清单安装；agents 随仓分发、手工拷入（Codex 插件不打包 agents）。

## 1. 前置：开启多代理特性

在 `~/.codex/config.toml` 加入：

```toml
[features]
multi_agent = true
```

不开启则子代理派发不可用，northstar 的 audit / code-review 环节将 BLOCKED。

## 2. 安装 agents（一次性拷贝）

把仓库内 `.codex/agents/` 下六个 TOML 拷入用户目录：

```bash
cp .codex/agents/*.toml ~/.codex/agents/
```

六个执行子代理及所钉型号（判断类高档 / 执行类中档 / 检索类低档）：

| agent | 型号 | effort |
|---|---|---|
| ns-auditor | gpt-5.6-sol | high |
| ns-reviewer | gpt-5.6-sol | high |
| ns-diagnostician | gpt-5.6-sol | high |
| ns-simplifier | gpt-5.6-sol | high |
| ns-implementer | gpt-5.6-terra | medium |
| ns-scout | gpt-5.6-luna | low |

所钉型号随 OpenAI 谱系迭代；若你的订阅档位无某型号权限，或想控制成本，可直接编辑 `~/.codex/agents/` 里的副本改型号 / 降 effort——分级原则（判断高 / 执行中 / 检索低）保持即可。

## 3. 安装 skills

经本仓库的 Codex 插件清单安装（见仓库 README 安装节）。

## 4. 验证

- `codex` 会话内确认六个 agent 可被点名委派；
- 平台执行说明见 `plugins/northstar/skills/implement/references/platform-codex.md`。
