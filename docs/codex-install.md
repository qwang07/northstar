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
mkdir -p ~/.codex/agents
cp .codex/agents/*.toml ~/.codex/agents/
```

拷贝是一次性的、无自动同步：仓库日后更新 TOML 需重新执行上述命令覆盖——覆盖会抹掉你本地的改档，重拷前先 diff 自查。

六个执行子代理及所钉型号（判断类高档 / 执行类中档 / 检索类低档）：

| agent | 型号 | effort |
|---|---|---|
| ns-auditor | gpt-5.6-sol | high |
| ns-reviewer | gpt-5.6-sol | high |
| ns-diagnostician | gpt-5.6-sol | high |
| ns-simplifier | gpt-5.6-sol | high |
| ns-implementer | gpt-5.6-terra | medium |
| ns-scout | gpt-5.6-luna | low |

所钉集需 ChatGPT **Plus 及以上**订阅（或 API-key）。免费档实测（2026-07）sol / luna 不可用（分别报 "not supported" / 404），可按同分级原则降档替代：判断类 → gpt-5.5 + high，检索类 → gpt-5.4-mini + low（均实测可用）。

所钉型号随 OpenAI 谱系迭代；若你的订阅档位无某型号权限，或想控制成本，可直接编辑 `~/.codex/agents/` 里的副本改型号 / 降 effort——分级原则（判断高 / 执行中 / 检索低）保持即可。注意：降档会相应降低该环节（评审 / 归因 / 精简）的判别力，取舍自担。

## 3. 安装 skills（已实测）

```bash
codex plugin marketplace add https://github.com/qwang07/northstar
codex plugin add northstar@northstar
```

## 3b. 日后更新（skills 与 agents 分开走）

```bash
codex plugin marketplace upgrade northstar
codex plugin add northstar@northstar        # 重装即升级 skills
cp .codex/agents/*.toml ~/.codex/agents/    # agents 无自动同步，重拷（覆盖本地改档，先 diff）
```

## 4. 验证（已实测）

```bash
codex exec "委派 ns-scout 子代理：列出本仓库顶层文件名。"
```

判定：会话真实 spawn 了 ns-scout 并返回文件列表（未开 `multi_agent` 时会拒绝委派，回查第 1 步）。平台执行说明见 `plugins/northstar/skills/implement/references/platform-codex.md`。
