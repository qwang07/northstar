# Codex CLI 前置配置（一次性）

northstar 在 Codex 侧只需两件事：开启多代理特性、装 skills。**不需要安装 agents**——0.9.2 起执行者由委派时的调用参数直接指定（`model` / `reasoning_effort` / `fork_turns`），仓库不再分发 agent 定义文件，也就没有"改了仓库要重拷 TOML"的手工同步。

## 1. 开启多代理特性（必须）

在 `~/.codex/config.toml` 加入：

```toml
[features]
multi_agent = true
```

不开启则委派不可用，northstar 的 audit / code-review / simplify 三处硬性子代理环节将 BLOCKED。

## 2. 安装 skills

```bash
codex plugin marketplace add https://github.com/qwang07/plugins
codex plugin add northstar@qwang07
```

## 3. 日后更新

```bash
codex plugin marketplace upgrade qwang07
codex plugin add northstar@qwang07        # 重装即升级 skills
```

绑定层（平台执行说明）随 skills 单源分发，无需另行更新。

## 4. 档位型号表

教条各相声明「推理档位」，本平台委派时按下表落成参数（权威表在 `plugins/northstar/skills/implement/references/platform-codex.md`，此处为安装期速查）：

| 档位 | 型号 | reasoning_effort |
|---|---|---|
| 判断类高档（评审 / 归因 / 精简） | gpt-5.6-sol | high |
| 执行类中档（实施） | gpt-5.6-terra | medium |
| 检索类低档（只读检索） | gpt-5.6-luna | low |

所钉集需 ChatGPT **Plus 及以上**订阅（或 API-key）。免费档实测（2026-07）sol / luna 不可用（分别报 "not supported" / 404），可按同分级原则降档替代：判断类 → gpt-5.5 + high，检索类 → gpt-5.4-mini + low（均实测可用）。降档会相应降低该环节的判别力，取舍自担。

## 5. 验证

```bash
codex exec "委派一个子代理（model=gpt-5.6-luna, reasoning_effort=low, fork_turns=none）：列出本仓库顶层文件名。"
```

判定：会话真实 spawn 了子代理并返回文件列表（未开 `multi_agent` 时会拒绝委派，回查第 1 步）。

## 6. 从 0.9.1 及更早版本升级

旧版本要求把六个 agent TOML 拷入用户目录，现已不再使用——清理掉即可，留着不会被调用但会造成困惑：

```bash
rm -f ~/.codex/agents/ns-{auditor,reviewer,implementer,simplifier,diagnostician,scout}.toml
```
