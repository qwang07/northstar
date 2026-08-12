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

SKILLS = {"brainstorming", "write-test", "audit", "implement", "simplify", "diagnose", "code-review", "deliver", "discover"}

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


# T1 教条层：九 skill 目录各含 SKILL.md（拓扑·教条层）
found_skills = {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}
check("T1 教条层九 SKILL.md 齐备", found_skills == SKILLS,
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

# ── T4 / T5 的量具分层（见 write-test「兑现类契约的两层量具」）────────────────
# 这两条守的是「平台执行说明逐项兑现，不接受空壳」——那是**兑现类契约**，本文件
# 只承担其可机械断言的一半：**覆盖齐全 + 落点互异 + 落点确含被翻译一侧没有的记号**。
# 三者足以判死"关键词各写一遍"的空壳，但证明不了兑现真能被消费。
# **兑现本身归消费方行为**：天真子代理只凭该说明能否派出参数正确的一次委派——
# 那是压测的活，不在本文件。切勿把下面的绿当成"兑现已验证"。
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


ROW_PAT = re.compile(r"^\|([^|\n]+)\|([^|\n]+)\|\s*$", re.M)
CAP_ROW_PAT = re.compile(r"^\|\s*(\d+)\s*\|([^|\n]+)\|([^|\n]+)\|\s*$", re.M)
TOKEN_PAT = re.compile(r"[A-Za-z][A-Za-z0-9_.\-]{1,}")


def mapping_rows(text):
    """「声明式约束 → 调用参数」表：{声明键: 右列原文}。键取 `X = Y` 的 Y。"""
    rows = {}
    for lhs, rhs in ROW_PAT.findall(text):
        m = re.search(r"(?:推理档位|工具面|零上下文)\s*=?\s*([^\s|（(]*)", lhs)
        key = m.group(1).strip() if m else ""
        if key in TIERS or key in ("只读", "读写"):
            rows.setdefault(key, (lhs.strip(), rhs.strip()))
    return rows


notes = {}
for plat in ("Claude Code", "Codex"):
    found = platform_notes(plat)
    notes[plat] = found
    if not found:
        check(f"T4 {plat} 平台执行说明存在", False, "未发现该平台的说明（含 I-平台能力表且标题点名平台）")
        continue
    for p, t in found:
        # T4a 能力表逐项：I-平台能力表须 1..6 项齐全，且每项兑现列非空（空格 / 破折号 / 待定不算）
        caps = {int(n): rhs.strip() for n, _, rhs in CAP_ROW_PAT.findall(t)}
        hollow = sorted(n for n in range(1, 7)
                        if n not in caps or caps[n].strip(" —-–*") in ("", "待定", "TBD", "N/A"))
        check(f"T4a {plat} 能力表 1-6 项各有非空兑现", not hollow,
              f"缺项或兑现列为空：{hollow}（逐项兑现不接受空壳）")

        # T4b 翻译表覆盖：三档位 + 两工具面各恰一行
        rows = mapping_rows(t)
        want = set(TIERS) | {"只读", "读写"}
        check(f"T4b {plat} 翻译表覆盖三档位与两工具面", set(rows) == want,
              f"实际 {sorted(rows)} ≠ 应有 {sorted(want)}")

        # T4c 三档位落点两两互异——同一个值写三遍等于没分级
        tier_vals = [rows[k][1] for k in TIERS if k in rows]
        check(f"T4c {plat} 三档位落点互异", len(set(tier_vals)) == len(tier_vals) == len(TIERS),
              f"落点重复或缺失：{tier_vals}")

        # T4d 三档位落点确含左列没有的平台记号——证明发生了翻译，而非把声明复述一遍
        norestate = []
        for k in TIERS:
            if k not in rows:
                continue
            lhs, rhs = rows[k]
            if not (set(TOKEN_PAT.findall(rhs)) - set(TOKEN_PAT.findall(lhs))):
                norestate.append(k)
        check(f"T4d {plat} 三档位落点非左列复述", not norestate,
              f"{norestate} 的右列无左列以外的平台记号——是复述不是翻译")

        # T4e 两工具面落点非空且非左列原样复述（其中只读的实质兑现由 T5 接手）
        faces_bad = [k for k in ("只读", "读写")
                     if k not in rows or rows[k][1].strip(" —-–*") in ("", rows[k][0].strip())]
        check(f"T4e {plat} 两工具面落点非空非复述", not faces_bad, f"空或复述：{faces_bad}")

# T5 只读工具面的事后核验（横切约束）——同样只测结构层：
# 核验节存在 + 步骤成序（≥3 步）+ 至少一条**可执行**的基线取值命令。
# 空壳文档写得出"基线 / 作废 / BLOCKED"这几个词，写不出可跑的取值命令与成序步骤；
# "不一致时判决真的被作废了吗"是行为，归压测，不在本文件。
STEP_PAT = re.compile(r"^\s*(\d+)\.\s+\S", re.M)
CMD_PAT = re.compile(r"`([^`\n]*\bgit\s+[^`\n]+)`")
for plat, found in notes.items():
    for p, t in found:
        sec = ""
        for chunk in re.split(r"^##\s+", t, flags=re.M)[1:]:
            head = chunk.splitlines()[0]
            if "只读" in head and "核验" in head:
                sec = chunk
                break
        if not sec:
            check(f"T5 {plat} 只读核验节存在", False,
                  "无「只读工具面的兑现与核验」小节——事前枚举不可得时，只读即无兑现")
            continue
        steps = STEP_PAT.findall(sec)
        # 命令须落在**第一步（记基线）**内：整节找命令会被后面的回滚命令顶替，
        # 于是"基线取值改成散文"这一变异捕获不到——已实测，故按步定位。
        parts = re.split(r"^\s*\d+\.\s+", sec, flags=re.M)
        first_step = parts[1] if len(parts) > 1 else ""
        cmds = CMD_PAT.findall(first_step)
        check(f"T5 {plat} 只读核验成序且记基线落到可执行取值", len(steps) >= 3 and bool(cmds),
              f"编号步骤 {len(steps)} 条（应 ≥3：记基线 / 明令 / 返回后比对）、"
              f"首步可执行取值命令 {len(cmds)} 条（应 ≥1）——基线取不出具体值，比对即无从谈起")

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
# 注：右列 models 取自平台说明而非手写字面量，这是**跨文档引用完整性**的固有形状，
# 不是镜像断言——两侧出自不同文档，一侧漂移另一侧未跟即红，正是它要抓的那次断裂。
# （镜像断言指两侧同源、恒真；此处硬钉型号反而会在仓外另立一处权威。）
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

# T11 教条指针：抽离了平台执行细节的教条正文须以指针引用平台执行说明，且指针有真实落点。
# 「正文须含指针字样」是词法契约，含词即正确量具；「落点存在」则逐平台断言，不只验一侧。
_has_pointer = "平台执行说明" in read(SKILLS_DIR / "implement/SKILL.md")
_empty = sorted(plat for plat, found in notes.items() if not found)
check("T11 implement 正文携带平台执行说明指针", _has_pointer, "教条正文缺指针字样")
check("T11 指针落点双平台齐备", not _empty, f"以下平台无说明可指：{_empty}")

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
