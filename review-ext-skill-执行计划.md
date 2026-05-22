# Review Ext Skill 创建执行计划

## 目标

基于 `profile_role_skill.md` 和 `skills-catalog.md`，创建智能技能路由器仓库 `review-ext-skill`，包含：
- ✅ 智能索引推荐功能（决策树 + 触发关键词 + 快速参考表）
- ✅ 所有 Review skill 的 references（含 TL;DR 摘要）
- ✅ 升级方案
- ✅ learns 踩坑记录

---

## Step 1: 下载 & 解压插件包

```bash
curl -L https://download.codebuddy.cn/plugin-marketplace/codebuddy-plugins-official.zip \
  -o /tmp/codebuddy-plugins-official.zip
mkdir -p /home/gql/tmp/codebuddy-skills
unzip -o /tmp/codebuddy-plugins-official.zip -d /home/gql/tmp/codebuddy-skills
```

---

## Step 2: 确认 GitHub 仓库

仓库名：`review-ext-skill`

---

## Step 3: 复制 profile_role_skill.md

**Review 角色 skill 列表**：

| Skill | 路径 | 级别 |
|-------|------|------|
| bmad-review | `agent-team-agile-workflow/agents/bmad-review.md` | P0 |
| code-reviewer | `comprehensive-review/agents/code-reviewer.md` | P0 |
| frontend-security-coder | `frontend-mobile-security/agents/frontend-security-coder.md` | P0 |
| backend-security-coder | `backend-api-security/agents/backend-security-coder.md` | P0 |
| receiving-code-review | `superpowers/skills/receiving-code-review/SKILL.md` | P0 |
| architect-review | `code-review-ai/agents/architect-review.md` | P1 |
| security-auditor | `full-stack-orchestration/agents/security-auditor.md` | P2 |

---

## Step 4: 确认 skill 路径存在

```bash
BASE=/home/gql/tmp/codebuddy-skills/external_plugins
PLUGINS=/home/gql/tmp/codebuddy-skills/plugins

for skill in \
  "agent-team-agile-workflow/agents/bmad-review.md" \
  "comprehensive-review/agents/code-reviewer.md" \
  "frontend-mobile-security/agents/frontend-security-coder.md" \
  "backend-api-security/agents/backend-security-coder.md" \
  "superpowers/skills/receiving-code-review/SKILL.md" \
  "code-review-ai/agents/architect-review.md" \
  "full-stack-orchestration/agents/security-auditor.md"
do
  if [ -f "$PLUGINS/$skill" ] || [ -f "$BASE/$skill" ]; then
    echo "✅ $skill"
  else
    echo "❌ $skill NOT FOUND"
  fi
done
```

---

## Step 5: 阅读 review_update.md

```bash
cat /home/gql/repos/gql-bots/docs/roles_skill/review_update.md
```

---

## Step 6: 阅读 skills-catalog.md

**Review 技能地图**：

| 场景 | 推荐 Skill | 理由 |
|------|-----------|------|
| 代码评审 | bmad-review | 评审规范核心 |
| 代码质量评审 | code-reviewer | 代码质量评审 |
| 前端安全 | frontend-security-coder | 前端安全 (XSS/CSP) |
| 后端安全 | backend-security-coder | 后端安全 (SQL注入/SSRF) |
| 反馈处理 | receiving-code-review | 反馈处理规范 |
| 架构合理性检查 | architect-review | 架构合理性检查 |
| DevSecOps | security-auditor | DevSecOps/OWASP |

---

## Step 7: 创建 review-ext-skill 仓库

### 7.0 仓库初始化（重要！）

```bash
# 1. 创建 Gitee 仓库
curl -X POST "https://gitee.com/api/v5/user/repos" \
  -d "name=review-ext-skill&description=Review技能索引路由器&private=false&auto_init=false" \
  -H "Authorization: token 4995bfdbb1093963081f117438cc9b3a"

# 2. 创建本地仓库
mkdir -p /home/gql/repos/review-ext-skill
cd /home/gql/repos/review-ext-skill
git init
git remote add origin https://gitee.com/ztanfo_admin/review-ext-skill.git
git remote add gitee https://ztanfo_admin:4995bfdbb1093963081f117438cc9b3a@gitee.com/ztanfo_admin/review-ext-skill.git

# 3. 创建目录结构
mkdir -p /home/gql/repos/review-ext-skill/learns
mkdir -p /home/gql/repos/review-ext-skill/references
```

### 7.1 SKILL.md 设计要点

```markdown
---
name: review-ext-skill
description: Review 技能索引路由器 - 接收任何评审任务，智能推荐最合适的 skill 并执行
version: 2.0.0
hermes:
  auto_route: true
---

# Review Ext Skill - 智能技能路由器

## ⚡ 快速路由（必读）

### 任务 → Skill 速查

| 你的任务（说人话） | → 推荐 Skill | 直接调用 |
|------------------|-------------|---------|
| "代码评审" | bmad-review | `hermes -p review -s bmad-review` |
| "评审代码质量" | code-reviewer | `hermes -p review -s code-reviewer` |
| "前端安全" | frontend-security-coder | `hermes -p review -s frontend-security-coder` |
| "后端安全" | backend-security-coder | `hermes -p review -s backend-security-coder` |
| "处理反馈" | receiving-code-review | `hermes -p review -s receiving-code-review` |
| "架构检查" | architect-review | `hermes -p review -s architect-review` |
| "安全审计" | security-auditor | `hermes -p review -s security-auditor` |

### 一句话触发规则

```
任务包含...         → 直接路由到...
────────────────────────────────────────────────────────────
"评审"、"review" → bmad-review
"代码质量"、"代码风格" → code-reviewer
"前端安全"、"xss"、"csp" → frontend-security-coder
"后端安全"、"sql注入"、"ssrf" → backend-security-coder
"反馈"、"处理评审意见" → receiving-code-review
"架构"、"架构检查" → architect-review
"安全"、"owasp"、"devsecops" → security-auditor
```

## 🔀 智能路由决策树

```
收到评审任务
    │
    ├─ 包含 "评审" / "review"
    │   └─→ bmad-review
    │       ├─ 代码质量 → code-reviewer
    │       ├─ 前端安全 → frontend-security-coder
    │       └─ 后端安全 → backend-security-coder
    │
    ├─ 包含 "代码质量" / "代码风格"
    │   └─→ code-reviewer
    │
    ├─ 包含 "前端安全" / "xss" / "csp"
    │   └─→ frontend-security-coder
    │
    ├─ 包含 "后端安全" / "sql注入" / "ssrf"
    │   └─→ backend-security-coder
    │
    ├─ 包含 "反馈" / "处理评审意见"
    │   └─→ receiving-code-review
    │
    ├─ 包含 "架构" / "架构检查"
    │   └─→ architect-review
    │
    └─ 包含 "安全" / "owasp" / "devsecops"
        └─→ security-auditor
```

## 📋 技能地图

| Skill | TL;DR | 级别 | 触发关键词 |
|-------|-------|------|-----------|
| bmad-review | 评审规范核心：评审流程、反馈规范 | P0 | 评审、review |
| code-reviewer | 代码质量评审：代码风格、最佳实践 | P0 | 代码质量、代码风格 |
| frontend-security-coder | 前端安全：XSS/CSRF/CSP/依赖漏洞 | P0 | 前端安全、xss、csp |
| backend-security-coder | 后端安全：SQL注入/SSRF/认证授权 | P0 | 后端安全、sql注入 |
| receiving-code-review | 反馈处理：评审意见处理、改进 | P0 | 反馈、处理评审意见 |
| architect-review | 架构合理性检查：架构模式、设计原则 | P1 | 架构、架构检查 |
| security-auditor | DevSecOps：OWASP Top 10、安全扫描 | P2 | 安全、owasp、devsecops |

## 🎯 场景化深度参考

### 详细参考（引用）

**自然语言示例 + Fallback + 组合流** → 见 `references/quick-reference.md`

### 快速决策速查

```
代码评审        → bmad-review
代码质量        → code-reviewer
前端安全        → frontend-security-coder
后端安全        → backend-security-coder
处理反馈        → receiving-code-review
架构检查        → architect-review
安全审计        → security-auditor
未知任务        → bmad-review + 询问澄清
```

---

## 🗣️ 自然语言触发示例（引用）

**详细示例** → 见 `references/quick-reference.md`

---

## ❓ Fallback 处理

**当任务无法匹配任何规则时**：

```markdown
1. 询问用户澄清：
   "这个任务是代码评审、安全检查、还是其他？"

2. 如果用户无法描述：
   → bmad-review（让评审核心帮你判断）
```

---

## 🔗 任务组合流

```
完整评审 → bmad-review
         → code-reviewer（质量）
         → frontend-security-coder（前端安全）
         → backend-security-coder（后端安全）

安全专项 → frontend-security-coder
         → backend-security-coder
         → security-auditor（如需全面审计）

处理反馈 → receiving-code-review
```

---

## 🔗 与 gql-review 主 skill 联动

当 Review 角色加载 `review-ext-skill` 时：

```markdown
1. 收到评审任务
2. 先加载 review-ext-skill（路由器）
3. 根据任务路由到具体 skill
4. 执行完成后返回 bmad-review 做汇总
```

**注意**：`review-ext-skill` 不会覆盖 `gql-review` 主 skill，它们协同工作。

---

## 🚨 常见错误

### 错误 1: 过度路由

```
❌ "用户说评审代码，路由到 bmad-review，
    然后又问用户要不要用 code-reviewer"
✓  直接路由到最可能的 skill，让用户决定是否深入
```

### 错误 2: 路由到不存在的 skill

```
❌ 根据关键词猜 skill 名称
✓  严格按照技能地图中的 skill 名称路由
```

### 错误 3: 忘记 Fallback

```
❌ 无法匹配时不知所措
✓  无法匹配时 → bmad-review（让评审核心帮你判断）
```

---

## 🔗 相关角色联动

| 角色 | 协作场景 |
|------|---------|
| **arc** | 架构评审：arc-ext-skill 设计 → review-ext-skill 评审架构 |
| **coder** | 代码评审：coder-ext-skill 自审 → review-ext-skill 正式评审 |
| **sm** | 需求评审：sm-ext-skill 评审需求 → review-ext-skill 评审实现方案 |
| **qa** | 测试评审：qa-ext-skill 测试 → review-ext-skill 评审测试覆盖 |

---

## 🗣️ 示例对话

### 示例 1: 路由到 bmad-review

```
用户：评审这个 PR
AI：分析：包含"评审"
     路由到 bmad-review
     执行：评审规范核心流程
```

### 示例 2: 路由到安全评审

```
用户：检查下有没有安全漏洞
AI：分析：包含"安全漏洞"
     路由到 frontend-security-coder
          → backend-security-coder
     执行：安全漏洞检查
```

### 示例 3: Fallback 处理

```
用户：帮我看看这段代码
AI：分析：包含"代码"
     但无法确定具体类型
     Fallback → bmad-review
     执行：评审核心判断任务类型
     反馈：这个任务是"代码质量评审"，建议用 code-reviewer
```

---

## 升级说明

查看 `update_readme.md` 了解如何同步最新 skill。

当前版本：v2.0.0

---

### 7.2 references 复制命令

```bash
BASE=/home/gql/tmp/codebuddy-skills/external_plugins
PLUGINS=/home/gql/tmp/codebuddy-skills/plugins
REFS=/home/gql/repos/review-ext-skill/references

mkdir -p $REFS

# P0 Skills
cp $PLUGINS/agent-team-agile-workflow/agents/bmad-review.md $REFS/bmad-review.md
cp $BASE/comprehensive-review/agents/code-reviewer.md $REFS/code-reviewer.md
cp $BASE/frontend-mobile-security/agents/frontend-security-coder.md $REFS/frontend-security-coder.md
cp $BASE/backend-api-security/agents/backend-security-coder.md $REFS/backend-security-coder.md
cp $BASE/superpowers/skills/receiving-code-review/SKILL.md $REFS/receiving-code-review.md

# P1 Skills
cp $BASE/code-review-ai/agents/architect-review.md $REFS/architect-review.md

# P2 Skills
cp $BASE/full-stack-orchestration/agents/security-auditor.md $REFS/security-auditor.md
```

### 7.3 references 添加 TL;DR

```bash
for f in references/*.md; do
  if ! grep -q "^<!-- TL;DR" "$f"; then
    case "$f" in
      bmad-review.md)
        echo "<!-- TL;DR: 评审规范核心：评审流程、反馈规范 -->" | cat - "$f" > temp && mv temp "$f"
        ;;
      code-reviewer.md)
        echo "<!-- TL;DR: 代码质量评审：代码风格、最佳实践 -->" | cat - "$f" > temp && mv temp "$f"
        ;;
      frontend-security-coder.md)
        echo "<!-- TL;DR: 前端安全：XSS/CSRF/CSP/依赖漏洞 -->" | cat - "$f" > temp && mv temp "$f"
        ;;
      backend-security-coder.md)
        echo "<!-- TL;DR: 后端安全：SQL注入/SSRF/认证授权 -->" | cat - "$f" > temp && mv temp "$f"
        ;;
      receiving-code-review.md)
        echo "<!-- TL;DR: 反馈处理：评审意见处理、改进 -->" | cat - "$f" > temp && mv temp "$f"
        ;;
      architect-review.md)
        echo "<!-- TL;DR: 架构合理性检查：架构模式、设计原则 -->" | cat - "$f" > temp && mv temp "$f"
        ;;
      security-auditor.md)
        echo "<!-- TL;DR: DevSecOps：OWASP Top 10、安全扫描 -->" | cat - "$f" > temp && mv temp "$f"
        ;;
    esac
  fi
done
```

---

## Step 8: 创建 learns/ 踩坑记录

**learns/README.md**：

```markdown
# Review Ext Skill 踩坑沉淀

## 🏷️ 按标签索引

## #路径确认

### bmad-review
- **位置**: `plugins/agent-team-agile-workflow/agents/bmad-review.md`
- **注意**: bmad 系列在 plugins 目录

### code-reviewer
- **位置**: `external_plugins/comprehensive-review/agents/code-reviewer.md`

### frontend-security-coder
- **位置**: `external_plugins/frontend-mobile-security/agents/frontend-security-coder.md`

### backend-security-coder
- **位置**: `external_plugins/backend-api-security/agents/backend-security-coder.md`

### receiving-code-review
- **位置**: `external_plugins/superpowers/skills/receiving-code-review/SKILL.md`

### architect-review
- **位置**: `external_plugins/code-review-ai/agents/architect-review.md`

### security-auditor
- **位置**: `external_plugins/full-stack-orchestration/agents/security-auditor.md`

## #source-区分

| 目录 | Skills |
|------|--------|
| `plugins/agent-team-agile-workflow/` | bmad-review |
| `external_plugins/comprehensive-review/` | code-reviewer |
| `external_plugins/frontend-mobile-security/` | frontend-security-coder |
| `external_plugins/backend-api-security/` | backend-security-coder |
| `external_plugins/superpowers/skills/` | receiving-code-review |
| `external_plugins/code-review-ai/` | architect-review |
| `external_plugins/full-stack-orchestration/` | security-auditor |
```

---

## Step 9: 创建 references/quick-reference.md

```bash
cat > /home/gql/repos/review-ext-skill/references/quick-reference.md << 'EOF'
<!-- TL;DR: 自然语言示例 + Fallback + 组合流快速参考 -->

# Review 技能路由快速参考

> 详细决策树见 SKILL.md 主文件

## 🗣️ 自然语言触发示例

| 用户实际说法 | → 路由到 | 说明 |
|-------------|---------|------|
| "评审这个 PR" | bmad-review | 评审规范 |
| "检查代码质量" | code-reviewer | 代码质量 |
| "有前端安全漏洞吗" | frontend-security-coder | XSS/CSRF |
| "后端安全检查" | backend-security-coder | SQL注入/SSRF |
| "处理评审意见" | receiving-code-review | 反馈处理 |
| "架构合理吗" | architect-review | 架构检查 |
| "做安全审计" | security-auditor | OWASP |

---

## 🔄 Fallback 处理

当任务**无法匹配**以上任何规则时：

```
未知任务
    │
    ├─ 询问用户澄清：
    │   "这个任务是代码评审、安全检查、还是其他？"
    │
    └─ 如果用户无法描述：
        └─→ bmad-review（让评审核心帮你判断）
```

**Fallback 规则**：
```markdown
无匹配时 → bmad-review → 让他判断用哪个 skill
```

---

## 🔗 任务组合流

### 组合 1: 完整代码评审

```
"评审这个 PR"
    │
    ├─ bmad-review（评审规范）
    │     ├─ code-reviewer（代码质量）
    │     ├─ frontend-security-coder（前端安全）
    │     └─ backend-security-coder（后端安全）
    │
    └─ architect-review（如需架构检查）
```

### 组合 2: 安全专项评审

```
"安全审计"
    │
    ├─ frontend-security-coder（前端）
    ├─ backend-security-coder（后端）
    └─ security-auditor（OWASP Top 10）
```

### 组合 3: 处理反馈

```
"收到评审意见"
    │
    └─ receiving-code-review
```

---

## ⚡ 快速决策速查卡

```
┌─────────────────────────────────────────────────────────────┐
│  任务类型              │  首选 Skill         │  辅助      │
├─────────────────────────────────────────────────────────────┤
│  代码评审              │  bmad-review       │            │
│  代码质量              │  code-reviewer     │            │
│  前端安全              │  frontend-secur..  │            │
│  后端安全              │  backend-secur..   │            │
│  处理反馈              │  receiving-code-r. │            │
│  架构检查              │  architect-review  │            │
│  安全审计              │  security-auditor  │            │
│  未知任务              │  bmad-review       │  询问澄清  │
└─────────────────────────────────────────────────────────────┘
```
EOF
```

---

## Step 10: 创建 update_readme.md 升级方案

```bash
cat > /home/gql/repos/review-ext-skill/update_readme.md << 'EOF'
# Review Ext Skill 升级方案

## 执行计划

详见 `review-ext-skill-执行计划.md`（详细步骤说明）

## 何时升级

1. `codebuddy-plugins-official.zip` 更新时
2. `gql-bots/shared/profile_role_skill.md` 变化时
3. `gql-bots/shared/skills-catalog.md` 更新时

## 升级步骤

### Step 1: 下载最新插件包

```bash
curl -L https://download.codebuddy.cn/plugin-marketplace/codebuddy-plugins-official.zip \
  -o /tmp/codebuddy-plugins-official.zip
unzip -o /tmp/codebuddy-plugins-official.zip -d /home/gql/tmp/codebuddy-skills
```

### Step 2: 同步 references

```bash
BASE=/home/gql/tmp/codebuddy-skills/external_plugins
PLUGINS=/home/gql/tmp/codebuddy-skills/plugins
REFS=/home/gql/repos/review-ext-skill/references

# 重新复制所有 skill 文件
# [同 Step 7 的复制命令]
```

### Step 3: 重新添加 TL;DR

```bash
for f in references/*.md; do
  if ! grep -q "^<!-- TL;DR" "$f"; then
    # 添加 TL;DR
    ...
  fi
done
```

### Step 4: 更新 quick-reference.md（如需要）

如果 skills-catalog.md 更新，同步更新 `references/quick-reference.md`。

### Step 5: 提交

```bash
cd /home/gql/repos/review-ext-skill
git add -A
git commit -m "chore: sync with latest codebuddy-plugins"
git push origin main
```

## 版本号规则

| 类型 | 规则 |
|------|------|
| 主版本 | skill 索引结构变化、决策树重构 |
| 次版本 | 新增/删除 skill、触发关键词更新 |
| 修订版 | 内容更新、TL;DR 更新 |

## 路径速查

| Skill | 源路径 |
|-------|--------|
| bmad-review | `plugins/agent-team-agile-workflow/agents/bmad-review.md` |
| code-reviewer | `external_plugins/comprehensive-review/agents/code-reviewer.md` |
| frontend-security-coder | `external_plugins/frontend-mobile-security/agents/frontend-security-coder.md` |
| backend-security-coder | `external_plugins/backend-api-security/agents/backend-security-coder.md` |
| receiving-code-review | `external_plugins/superpowers/skills/receiving-code-review/SKILL.md` |
| architect-review | `external_plugins/code-review-ai/agents/architect-review.md` |
| security-auditor | `external_plugins/full-stack-orchestration/agents/security-auditor.md` |
EOF
```

---

## Step 11: 创建 README.md

```bash
cat > /home/gql/repos/review-ext-skill/README.md << 'EOF'
# Review Ext Skill

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/platforms-hermes-blue.svg)](#)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](SKILL.md)
[![Review Skills](https://img.shields.io/badge/Review_Skills-7-orange.svg)](#)
[![Auto Route](https://img.shields.io/badge/Auto_Route-Enabled-blue.svg)](#)

代码评审技能索引路由器 - 接收任何评审任务，智能推荐最合适的 skill 并执行。

## 目录

- [快速开始](#快速开始)
- [技能地图](#技能地图)
- [工作流](#工作流)
- [升级](#升级)

## 快速开始

```bash
# 安装
git clone https://gitee.com/ztanfo_admin/review-ext-skill.git ~/.hermes/profiles/review/skills/review-ext-skill

# 使用
hermes -p review -s review-ext-skill
```

## 技能地图

| Skill | 说明 | 级别 |
|-------|------|------|
| bmad-review | 评审规范核心 | P0 |
| code-reviewer | 代码质量评审 | P0 |
| frontend-security-coder | 前端安全 | P0 |
| backend-security-coder | 后端安全 | P0 |
| receiving-code-review | 反馈处理 | P0 |
| architect-review | 架构合理性检查 | P1 |
| security-auditor | DevSecOps/OWASP | P2 |

## 工作流

详见 [SKILL.md](SKILL.md)

## 升级

详见 [update_readme.md](update_readme.md)
EOF
```

---

## Step 12: Git 提交

```bash
cd /home/gql/repos/review-ext-skill
git add -A
git commit -m "feat: initial review-ext-skill with all Review skills"
git push origin main
```

---

## 验证清单

- [ ] 下载解压成功
- [ ] GitHub 仓库已创建/更新
- [ ] 所有 7 个 skill 路径验证通过
- [ ] references/ 包含所有 skill 文件（含 TL;DR）
- [ ] references/quick-reference.md 已创建
- [ ] SKILL.md 包含智能索引：
  - [ ] 一句话触发规则
  - [ ] 决策树
  - [ ] 技能地图
  - [ ] 场景化深度参考
  - [ ] Fallback 处理
  - [ ] 任务组合流
  - [ ] 主 skill 联动
- [ ] learns/ 有踩坑记录
- [ ] update_readme.md 有升级方案
- [ ] README.md 已美化
- [ ] git push 成功
