#!/usr/bin/env python3
"""northstar 项目级结构测试——从 README「跨平台拓扑」节派生。

每条测试标注其指回的 README 条款。发现式断言（不钉实现自由的文件布局）。
运行：python3 tests/structure.py；全绿退出码 0，任一红非 0。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "plugins/northstar/skills"

SKILLS = {"brainstorming", "write-test", "audit", "implement", "simplify", "diagnose", "code-review", "deliver"}

# 声明式约束（绑定层删除后的单源）：哪些相派发、各自工具面与推理档位
# —— 权威见各 SKILL.md 的「派发声明」，本表是其可机械断言的投影
DISPATCH = {
    "audit":       ("只读", "判断类高档"),
    "code-review": ("只读", "判断类高档"),
    "simplify":    ("读写", "判断类高档"),
    "implement":   ("读写", "执行类中档"),
    "diagnose":    ("读写", "判断类高档"),
}
TIERS = {"判断类高档", "执行类中档", "检索类低档"}
FACE_PAT = r"工具面 = (只读|读写)"
TIER_PAT = r"推理档位 = (判断类高档|执行类中档|检索类低档)"

# 横切约束 C1：教条正文禁现平台专属名词（工具名 / 配置字段 / 调用语法）
FORBIDDEN = [
    r"\bfrontmatter\b", r"\bTask\b", r"\bSlashCommand\b", r"\bsubagent_type\b",
    r"\bopus\b", r"\bsonnet\b", r"\bhaiku\b", r"\bgpt-\d", r"model_reasoning_effort",
    r"Claude Code", r"\bCodex\b", r"\.claude\b", r"\.codex\b",
    r"CLAUDE\.md", r"AGENTS\.md", r"marketplace", r"plugin\.json",
    r"\bworkflow\b", r"\binline\b", r"\bteam\b", r"\bns-[a-z]+\b",
]

failures = []


def check(name, ok, reason=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f" —— {reason}"))
    if not ok:
        failures.append(name)


def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""


# T1 教条层：八 skill 目录各含 SKILL.md（拓扑·教条层）
found_skills = {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}
check("T1 教条层八 SKILL.md 齐备", found_skills == SKILLS,
      f"实际 {sorted(found_skills)} ≠ 声明 {sorted(SKILLS)}")

# T2 绑定层无 agent 定义文件（拓扑·绑定层「不设 agent 定义文件」）——断言不存在，防复活
stray_dirs = [p for p in ROOT.rglob("agents") if p.is_dir() and ".git" not in p.parts]
check("T2 无 agent 定义目录", not stray_dirs,
      f"发现 {[str(p.relative_to(ROOT)) for p in stray_dirs]}——人格应由派发者按教条现场组装，不另存副本")
stray_agent_files = [p for p in ROOT.rglob("ns-*") if ".git" not in p.parts]
check("T2 无 ns-* 执行者定义残留", not stray_agent_files,
      f"发现 {[str(p.relative_to(ROOT)) for p in stray_agent_files]}")

# T3 声明式约束：派发相各自声明工具面 + 推理档位；枚举齐全且无越界（能力表第 6 项）
declared = {}
for s in sorted(SKILLS):
    text = read(SKILLS_DIR / s / "SKILL.md")
    faces, tiers = set(re.findall(FACE_PAT, text)), set(re.findall(TIER_PAT, text))
    if faces or tiers:
        declared[s] = (faces, tiers)
check("T3 派发声明枚举齐全且无越界", set(declared) == set(DISPATCH),
      f"实际携带派发声明 {sorted(declared)} ≠ 声明 {sorted(DISPATCH)}")
for s, (want_face, want_tier) in DISPATCH.items():
    faces, tiers = declared.get(s, (set(), set()))
    check(f"T3 {s} 声明工具面={want_face} 档位={want_tier}",
          faces == {want_face} and tiers == {want_tier},
          f"实际 工具面={sorted(faces)} 档位={sorted(tiers)}")

# T4 平台执行说明（绑定层唯一载体）：每平台一份，逐项兑现不接受空壳——
# 强断言：须含 I-平台能力表 + 全部三档位的翻译落点 + 两种工具面，缺一即空壳。
def platform_notes(platform_word):
    found = []
    for p in ROOT.rglob("*.md"):
        if ".git" in p.parts or p.name in ("README.md", "README.en.md"):
            continue
        t = read(p)
        title = t.lstrip().splitlines()[0] if t.strip() else ""
        if "I-平台能力表" in t and platform_word in title:
            found.append((p, t))
    return found

notes = {}
for plat in ("Claude Code", "Codex"):
    found = platform_notes(plat)
    notes[plat] = found
    ok = len(found) >= 1 and all(
        all(tier in t for tier in TIERS) and "只读" in t and "读写" in t for _, t in found)
    check(f"T4 {plat} 平台执行说明存在且逐项兑现", ok,
          "缺说明，或未覆盖全部三档位与两种工具面的调用参数翻译")

# T5 只读工具面以基线比对兑现（横切约束）：双平台说明皆须给出核验机制与失败处置
for plat, found in notes.items():
    ok = bool(found) and all(
        "基线" in t and "作废" in t and "BLOCKED" in t for _, t in found)
    check(f"T5 {plat} 声明只读核验（基线比对 + 判决作废 + BLOCKED）", ok,
          "只读工具面无事后核验条款——事前枚举不可得时，只读即无兑现")

# T6 分发层（拓扑·分发层）：编目在外部 marketplace（qwang07/plugins，git-subdir 收录
# plugins/northstar——插件根即 plugins/northstar，双端共认）；仓内只留插件清单。
check("T6 Claude 插件清单存在", (ROOT / "plugins/northstar/.claude-plugin/plugin.json").is_file(),
      "缺 plugins/northstar/.claude-plugin/plugin.json")
check("T6 仓内 marketplace 已退役", not (ROOT / ".claude-plugin/marketplace.json").exists(),
      "仓内 marketplace 复活——编目已移至 qwang07/plugins，双重编目 = 同插件双上架")
stray_codex = [p for p in ROOT.rglob(".codex-plugin/plugin.json") if ".git" not in p.parts]
check("T6 Codex 重定向清单已退役", not stray_codex,
      f"发现 {[str(p) for p in stray_codex]}——git-subdir 下插件根即 plugins/northstar，无需重定向清单")

# T7 横切 C1：教条正文禁现平台专属名词（持续不变量，可机械断言）
for s in sorted(SKILLS):
    hits = sorted({pat for pat in FORBIDDEN if re.search(pat, read(SKILLS_DIR / s / "SKILL.md"))})
    check(f"T7 {s} 正文无平台专属名词", not hits, f"命中禁词 {hits}")

# T8 引用完整性：双语 README 不得残留执行者具名（绑定层已无定义文件）
for readme in ("README.md", "README.en.md"):
    names = sorted(set(re.findall(r"\bns-[a-z]+\b", read(ROOT / readme))))
    check(f"T8 {readme} 无执行者具名残留", not names, f"残留 {names}")

# T9 Codex 安装指引：存在且各档位型号与平台说明一致（C4 + 安装节）
codex_note = "\n".join(t for _, t in notes.get("Codex", []))
guides = [p for p in ROOT.rglob("*.md")
          if ".git" not in p.parts and p.name not in ("README.md", "README.en.md")
          and "multi_agent" in read(p) and "I-平台能力表" not in read(p)]
if not guides:
    check("T9 Codex 安装指引存在", False, "未发现含多代理前置配置的指引文档")
else:
    guide_text = "\n".join(read(p) for p in guides)
    models = sorted(set(re.findall(r"gpt-5[\w.-]*", codex_note)))
    check("T9 平台说明已钉各档位型号", len(models) >= 3, f"实际钉出 {models}（三档位应各有型号）")
    missing = [m for m in models if m not in guide_text]
    check("T9 指引声明平台说明所钉全部型号", not missing, f"指引未声明 {missing}")

# T11 教条指针：抽离了平台执行细节的教条正文须以指针引用平台执行说明，且指针有真实落点
check("T11 implement 指针指向真实平台执行说明",
      "平台执行说明" in read(SKILLS_DIR / "implement/SKILL.md") and bool(notes.get("Claude Code")),
      "缺指针字样，或指针无落点（Claude 侧说明不存在）")

# T12 收敛阀阈值复述（README「节奏·回路收敛阀」的显式例外条款）：
# 例外范围恰为枚举五相（契约回踢类），各处数值与 README 一致；枚举外教条不得携带同款复述。
VALVE_SET = {"brainstorming", "write-test", "audit", "implement", "code-review", "deliver"}
VALVE_PAT = r"阈值（默认 (\d+) 次）"
readme_vals = set(re.findall(VALVE_PAT, read(ROOT / "README.md")))
check("T12 README 声明阈值", len(readme_vals) == 1,
      f"README 阈值数值 {sorted(readme_vals)}（应恰一种）")
valve_carriers = {}
for s in sorted(SKILLS):
    vals = set(re.findall(VALVE_PAT, read(SKILLS_DIR / s / "SKILL.md")))
    if vals:
        valve_carriers[s] = vals
check("T12 阈值复述枚举齐全且无越界", set(valve_carriers) == VALVE_SET,
      f"实际携带 {sorted(valve_carriers)} ≠ 枚举 {sorted(VALVE_SET)}")
all_vals = readme_vals.union(*valve_carriers.values()) if valve_carriers else readme_vals
check("T12 阈值各处数值一致", len(all_vals) == 1, f"数值不一 {sorted(all_vals)}")
if len(all_vals) == 1:
    _v = next(iter(all_vals))
    check("T12 英文版阈值同值", f"default {_v}" in read(ROOT / "README.en.md"),
          f"README.en.md 未见 default {_v}")

print(f"\n{'全绿' if not failures else f'{len(failures)} 红'}：共 {len(failures)} 失败")
sys.exit(1 if failures else 0)
