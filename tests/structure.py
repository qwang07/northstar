#!/usr/bin/env python3
"""northstar 项目级结构测试——从 README「跨平台拓扑」节派生。

每条测试标注其指回的 README 条款。发现式断言（不钉实现自由的文件布局）。
运行：python3 tests/structure.py；全绿退出码 0，任一红非 0。
"""
import re
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit("环境缺失：需 Python 3.11+（tomllib）。环境错不伪装成契约红。")

try:
    import tomllib
except ModuleNotFoundError:  # < 3.11
    sys.exit("环境缺失：需 Python 3.11+（tomllib）。环境错不伪装成契约红。")

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "plugins/northstar/skills"
AGENTS_DIR = ROOT / "plugins/northstar/agents"

SKILLS = {"brainstorming", "write-test", "audit", "implement", "diagnose", "code-review"}
AGENTS = {"ns-scout", "ns-diagnostician", "ns-auditor", "ns-implementer", "ns-simplifier", "ns-reviewer"}
# 能力表第 5 项：判断类高档（评审 / 归因 / 精简）、执行类中档、检索类低档
TIER = {
    "ns-auditor": "judgment", "ns-reviewer": "judgment",
    "ns-diagnostician": "judgment", "ns-simplifier": "judgment",
    "ns-implementer": "execution", "ns-scout": "retrieval",
}
CLAUDE_MODEL = {"judgment": "opus", "execution": "sonnet", "retrieval": "haiku"}
CODEX_EFFORT = {"judgment": {"high", "xhigh"}, "execution": {"medium"}, "retrieval": {"low", "minimal"}}

# 横切约束 C1：教条正文禁现平台专属名词（工具名 / 配置字段 / 调用语法）
FORBIDDEN = [
    r"\bfrontmatter\b", r"\bTask\b", r"\bSlashCommand\b", r"\bsubagent_type\b",
    r"\bopus\b", r"\bsonnet\b", r"\bhaiku\b", r"\bgpt-\d", r"model_reasoning_effort",
    r"Claude Code", r"\bCodex\b", r"\.claude\b", r"\.codex\b",
    r"CLAUDE\.md", r"AGENTS\.md", r"marketplace", r"plugin\.json",
    r"\bworkflow\b", r"\binline\b",
]

failures = []


def check(name, ok, reason=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f" —— {reason}"))
    if not ok:
        failures.append(name)


def read_frontmatter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    return dict(
        (k.strip(), v.strip())
        for k, v in (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    ) if m else {}


# T1 教条层：六 skill 目录各含 SKILL.md（拓扑·教条层）
found_skills = {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}
check("T1 教条层六 SKILL.md 齐备", found_skills == SKILLS,
      f"实际 {sorted(found_skills)} ≠ 声明 {sorted(SKILLS)}")

# T2 Claude 绑定层：agents/ 文件集恰好等于花名册（拓扑·绑定层）
found_agents = {p.stem for p in AGENTS_DIR.glob("*.md")}
check("T2 Claude 绑定层六 agent 齐备", found_agents == AGENTS,
      f"实际 {sorted(found_agents)} ≠ 声明 {sorted(AGENTS)}")

# T3 Claude 绑定分级：frontmatter model 全等匹配分级规则（能力表第 5 项）
for a in sorted(AGENTS):
    p = AGENTS_DIR / f"{a}.md"
    model = read_frontmatter(p).get("model") if p.exists() else None
    want = CLAUDE_MODEL[TIER[a]]
    check(f"T3 {a} 钉 {want}", model == want, f"实际 model={model!r}")

# T4/T5 Codex 绑定层：仓库内发现 6 个 TOML，name 集合=花名册；每个钉具体型号+effort 档位（拓扑·绑定层 + C4）
tomls = {}
for p in ROOT.rglob("*.toml"):
    if ".git" in p.parts:
        continue
    try:
        data = tomllib.load(p.open("rb"))
    except Exception:
        continue
    if data.get("name") in AGENTS:
        tomls[data["name"]] = data
check("T4 Codex 绑定层六 agent TOML 齐备", set(tomls) == AGENTS,
      f"实际发现 {sorted(tomls)} ≠ 声明 {sorted(AGENTS)}")
for a in sorted(AGENTS):
    d = tomls.get(a)
    if d is None:
        check(f"T5 {a} TOML 钉型号+档位", False, "TOML 缺失")
        continue
    model, effort = d.get("model", ""), d.get("model_reasoning_effort", "")
    want_efforts = CODEX_EFFORT[TIER[a]]
    check(f"T5 {a} TOML 钉型号+档位", bool(model) and effort in want_efforts,
          f"model={model!r}, effort={effort!r}（应为 {sorted(want_efforts)} 之一且型号非空）")

# T6 分发层双侧（拓扑·分发层）：
# Claude Code 侧：.claude-plugin/ marketplace（结构树钉死路径）
check("T6 Claude marketplace 清单存在", (ROOT / ".claude-plugin/marketplace.json").is_file(),
      "缺 .claude-plugin/marketplace.json")
check("T6 Claude 插件清单存在", (ROOT / "plugins/northstar/.claude-plugin/plugin.json").is_file(),
      "缺 plugins/northstar/.claude-plugin/plugin.json")
# Codex 侧：清单路径遵平台约定 .codex-plugin/plugin.json（目录布局自由 → 只钉尾部）
codex_manifests = [p for p in ROOT.rglob(".codex-plugin/plugin.json") if ".git" not in p.parts]
check("T6 Codex 插件清单存在", len(codex_manifests) >= 1, "仓库内未发现 .codex-plugin/plugin.json")

# T9 Codex 安装指引：存在且声明所钉型号（C4 + 安装节）。发现式：含 .codex/agents 路径
# 且列出全部六 agent 名的 Markdown 即指引；其须含每个 TOML 所钉型号字串。
guides = [
    p for p in ROOT.rglob("*.md")
    if ".git" not in p.parts and p.name != "README.md" and p.name != "README.en.md"
    and ".codex/agents" in (t := p.read_text(encoding="utf-8"))
    and all(a in t for a in AGENTS)
]
if not guides:
    check("T9 Codex 安装指引存在", False, "未发现含 .codex/agents 路径且列全六 agent 的指引文档")
else:
    guide_text = "\n".join(p.read_text(encoding="utf-8") for p in guides)
    for a in sorted(AGENTS):
        model = tomls.get(a, {}).get("model", "")
        check(f"T9 指引声明 {a} 所钉型号", bool(model) and model in guide_text,
              f"TOML model={model!r} 未在指引中声明" if model else "TOML 缺失，无型号可核")

# T7 横切 C1：教条正文禁现平台专属名词（持续不变量，可机械断言）
for s in sorted(SKILLS):
    p = SKILLS_DIR / s / "SKILL.md"
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    hits = sorted({pat for pat in FORBIDDEN if re.search(pat, text)})
    check(f"T7 {s} 正文无平台专属名词", not hits, f"命中禁词 {hits}")

# T10 平台执行说明：每平台一份（绑定层扩义条款），逐项兑现不接受空壳——
# 发现式：非 README 的 Markdown，含"I-平台能力表"且含平台名；强断言：兑现声明须
# 引用全部六个 agent（能力表 1-4 项的执行者 + 第 5 项分级的载体），缺一即空壳。
def platform_notes(platform_word):
    found = []
    for p in ROOT.rglob("*.md"):
        if ".git" in p.parts or p.name in ("README.md", "README.en.md"):
            continue
        t = p.read_text(encoding="utf-8")
        # 平台归属以标题行判定——正文提及他平台（如交叉指针）不得冒充他平台的说明
        title = t.lstrip().splitlines()[0] if t.strip() else ""
        if "I-平台能力表" in t and platform_word in title and all(a in t for a in AGENTS):
            found.append(p)
    return found

claude_notes = platform_notes("Claude")
check("T10 Claude 平台执行说明存在且逐项兑现", len(claude_notes) >= 1,
      "未发现含 I-平台能力表 + 全部六 agent 兑现声明的 Claude 侧说明")
check("T10 Codex 平台执行说明存在且逐项兑现", len(platform_notes("Codex")) >= 1,
      "未发现含 I-平台能力表 + 全部六 agent 兑现声明的 Codex 侧说明")

# T11 教条指针：抽离了平台执行细节的教条正文须以指针引用平台执行说明，且指针有真实落点
impl_text = (SKILLS_DIR / "implement/SKILL.md").read_text(encoding="utf-8")
check("T11 implement 指针指向真实平台执行说明", "平台执行说明" in impl_text and len(claude_notes) >= 1,
      "缺指针字样，或指针无落点（Claude 侧说明不存在）")

# T8 引用完整性：双语 README 花名册 == agents/ 文件集（持续不变量·跨文档引用完整性）
for readme in ["README.md", "README.en.md"]:
    names = set(re.findall(r"\bns-[a-z]+\b", (ROOT / readme).read_text(encoding="utf-8")))
    check(f"T8 {readme} 花名册与 agents/ 全等", names == found_agents,
          f"README 引用 {sorted(names)} ≠ 目录 {sorted(found_agents)}")

print(f"\n{'全绿' if not failures else f'{len(failures)} 红'}：共 {len(failures)} 失败")
sys.exit(1 if failures else 0)
