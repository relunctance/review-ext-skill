---
name: review-ext-skill
description: Review 技能索引路由器 - 接收任何评审任务，智能推荐最合适的 skill 并执行
version: 2.0.0
author: relunctance
license: MIT
category: gql-bots
tags:
  - review
  - code-review
  - security
  - skill-router
  - gql-bots
  - intelligent-router
hermes:
  platforms:
    hermes: true
  auto_route: true
---

# Review Ext Skill - 智能技能路由器

> **核心定位**：Review 角色的中央路由器。任何评审任务进来，先查这里，再路由到具体 skill。

---

## ⚡ TL;DR 速查索引

| 你要做的事 | 直接路由 | 说明 |
|------------|---------|------|
| 评审代码/PR | bmad-review | 从评审核心开始 |
| 代码质量/风格 | code-reviewer | 最佳实践 |
| XSS/CSRF/CSP | frontend-security-coder | 前端安全 |
| SQL注入/SSRF | backend-security-coder | 后端安全 |
| 处理评审反馈 | receiving-code-review | 反馈改进 |
| 架构合理性 | architect-review | 设计原则 |
| 全面安全审计 | security-auditor | OWASP |
| 不知道用哪个 | bmad-review | 让它帮你判断 |

---

## ⚡ 快速路由（必读）

### 任务 → Skill 速查

| 你的任务（说人话） | → 推荐 Skill | 直接调用 |
|------------------|-------------|---------|
| "评审这个 PR" | bmad-review | `hermes -p review -s bmad-review` |
| "检查代码质量" | code-reviewer | `hermes -p review -s code-reviewer` |
| "前端安全检查" | frontend-security-coder | `hermes -p review -s frontend-security-coder` |
| "后端安全检查" | backend-security-coder | `hermes -p review -s backend-security-coder` |
| "处理评审意见" | receiving-code-review | `hermes -p review -s receiving-code-review` |
| "检查架构合理性" | architect-review | `hermes -p review -s architect-review` |
| "全面安全审计" | security-auditor | `hermes -p review -s security-auditor` |

### 一句话触发规则（增强版）

```
任务包含...              → 直接路由到...
────────────────────────────────────────────────────────────────────────────
# 代码评审
"评审"、"review"、"pr"、"mr" → bmad-review
"代码质量"、"代码风格"、"风格" → code-reviewer
"单元测试"、"测试覆盖" → code-reviewer

# 安全评审
"xss"、"跨站"、"csrf"、"csp" → frontend-security-coder
"sql注入"、"注入"、"ssrf" → backend-security-coder
"安全"、"审计"、"owasp"、"devsecops" → security-auditor
"漏洞"、"扫描"、"依赖安全" → security-auditor
"鉴权"、"授权"、"oauth"、"jwt" → backend-security-coder

# 架构评审
"架构"、"架构检查"、"架构评审" → architect-review
"设计模式"、"SOLID"、"DRY" → architect-review
"性能"、"瓶颈"、"优化" → architect-review

# 反馈处理
"反馈"、"评审意见"、"处理" → receiving-code-review
"改进"、"重构" → receiving-code-review

# 测试评审
"测试覆盖"、"测试质量" → bmad-review
"单元测试"、"集成测试" → code-reviewer
```

---

## 🔀 智能路由决策树

```
收到评审任务
    │
    ├─ 🎯 代码评审？
    │   └─ bmad-review
    │       ├─ 代码质量/风格 → code-reviewer
    │       ├─ 测试覆盖 → code-reviewer
    │       └─ 返回 bmad-review 汇总
    │
    ├─ 🎯 安全评审？
    │   ├─ 前端相关（XSS/CSRF/CSP） → frontend-security-coder
    │   ├─ 后端相关（SQL/SSRF/鉴权） → backend-security-coder
    │   └─ 全面审计 → security-auditor
    │
    ├─ 🎯 架构评审？
    │   └─ architect-review
    │       ├─ 设计模式
    │       ├─ SOLID/DRY
    │       └─ 性能分析
    │
    ├─ 🎯 反馈处理？
    │   └─ receiving-code-review
    │
    └─ ❓ 不知道
        └─ bmad-review + 询问澄清
```

---

## 📋 技能地图

| Skill | TL;DR | 级别 | 触发关键词 |
|-------|-------|------|-----------|
| bmad-review | 评审规范核心：评审流程、反馈规范 | P0 | 评审、review、pr |
| code-reviewer | 代码质量评审：代码风格、最佳实践 | P0 | 代码质量、代码风格 |
| frontend-security-coder | 前端安全：XSS/CSRF/CSP/依赖漏洞 | P0 | 前端安全、xss、csp |
| backend-security-coder | 后端安全：SQL注入/SSRF/认证授权 | P0 | 后端安全、sql注入 |
| receiving-code-review | 反馈处理：评审意见处理、改进 | P0 | 反馈、处理评审意见 |
| architect-review | 架构合理性检查：架构模式、设计原则 | P1 | 架构、架构检查 |
| security-auditor | DevSecOps：OWASP Top 10、安全扫描 | P2 | 安全、owasp、devsecops |

---

## 🎯 场景化深度参考（4大场景）

### 场景 1: 代码评审 🔍

```
需求：评审一个 PR
    │
    └─ bmad-review（评审核心）
          ├─ 代码质量 → code-reviewer
          │     → 代码风格、最佳实践
          │     → 单元测试覆盖
          │
          ├─ 安全检查
          │     → frontend-security-coder（如有前端）
          │     → backend-security-coder（如有后端）
          │
          └─ 返回 bmad-review 汇总反馈
```

### 场景 2: 安全评审 🔒

```
需求：检查安全漏洞
    │
    ├─ 前端安全？
    │   └─ frontend-security-coder
    │         → XSS/CSRF/CSP
    │         → 依赖漏洞检查
    │
    ├─ 后端安全？
    │   └─ backend-security-coder
    │         → SQL注入/SSRF
    │         → 认证/授权问题
    │
    └─ 全面审计？
        └─ security-auditor
              → OWASP Top 10
              → 安全扫描
```

### 场景 3: 架构评审 🏗️

```
需求：评审架构合理性
    │
    └─ architect-review
          ├─ 设计模式检查
          │     → SOLID 原则
          │     → DRY/YAGNI
          │
          ├─ 性能分析
          │     → 瓶颈识别
          │     → 优化建议
          │
          └─ 技术债评估
```

### 场景 4: 处理反馈 📝

```
需求：处理评审意见
    │
    └─ receiving-code-review
          ├─ 逐条处理反馈
          ├─ 代码改进
          └─ 回复评审者
```

### 快速决策速查

```
┌────────────────────────────────────────────────────────────┐
│  场景              │  路由顺序                              │
├────────────────────────────────────────────────────────────┤
│  PR/代码评审        │  bmad-review → code-reviewer         │
│  安全漏洞检查       │  frontend/backend-security-coder      │
│  全面安全审计       │  security-auditor                    │
│  架构合理性检查     │  architect-review                    │
│  处理评审反馈       │  receiving-code-review                │
│  测试覆盖评审       │  bmad-review → code-reviewer         │
│  性能评审           │  architect-review                    │
│  未知任务           │  bmad-review + 询问澄清              │
└────────────────────────────────────────────────────────────┘
```

---

## ❓ Fallback 处理

当任务**无法匹配**以上任何规则时：

```
未知任务
    │
    ├─ 询问用户澄清：
    │   "这个任务是代码评审、安全检查、还是架构评审？"
    │
    └─ 如果用户无法描述：
        └─→ bmad-review（让评审核心帮你判断）
```

---

## 🔗 任务组合流

### 组合 1: 完整代码评审

```
"完整评审这个 PR"
    │
    └─ bmad-review
          ├─ code-reviewer（代码质量）
          ├─ frontend-security-coder（如有前端）
          ├─ backend-security-coder（如有后端）
          └─ architect-review（如需架构检查）
```

### 组合 2: 安全专项评审

```
"检查安全漏洞"
    │
    ├─ frontend-security-coder（前端）
    ├─ backend-security-coder（后端）
    └─ security-auditor（全面审计）
```

### 组合 3: 评审反馈处理

```
"处理评审意见"
    │
    └─ receiving-code-review
          ├─ 逐条处理
          ├─ 代码改进
          └─ 提交回复
```

---

## 🔗 与 gql-review 主 skill 联动

**注意**：`review-ext-skill` 不会覆盖 `gql-review` 主 skill，它们协同工作。

```
┌─────────────────────────────────────────────────────────────┐
│  gql-review 主 skill                                        │
│    │                                                        │
│    ├─ 通用评审任务 → review-ext-skill（路由）                │
│    │              └─→ 具体 skill 执行                         │
│    │                                                        │
│    └─ 特定技能任务 → 直接调用具体 skill                       │
└─────────────────────────────────────────────────────────────┘
```

**何时使用 review-ext-skill**：
- 任务模糊，需要判断用哪个 skill
- 复杂任务需要多 skill 组合
- 不确定某个 skill 是否适用

**何时直接调用具体 skill**：
- 任务明确，比如"检查 XSS 漏洞"
- 已确定需要哪个 skill
- 只需要单个 skill

---

## 📖 References 快速索引

详见 `references/quick-reference.md`（自然语言示例 + Fallback + 组合流）

每个 skill 文件都有 TL;DR 摘要：

| Skill | TL;DR | 说明 |
|-------|-------|------|
| bmad-review.md | 评审规范核心 | 评审流程、反馈规范 |
| code-reviewer.md | 代码质量评审 | 代码风格、最佳实践 |
| frontend-security-coder.md | 前端安全 | XSS/CSRF/CSP |
| backend-security-coder.md | 后端安全 | SQL注入/SSRF |
| receiving-code-review.md | 反馈处理 | 评审意见处理 |
| architect-review.md | 架构评审 | 架构模式、设计原则 |
| security-auditor.md | 安全审计 | OWASP Top 10 |

---

## 🚨 常见错误

| 错误 | 正确做法 |
|------|---------|
| 直接说"评审代码" | 说明评审什么（质量？安全？架构？） |
| 不确定用哪个 skill | → bmad-review 让它帮你判断 |
| 过度路由 | 直接路由到最可能的 skill |
| 忘记 Fallback | 无法匹配时 → bmad-review |

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
AI：分析：包含"评审"、"PR"
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

查看 [update_readme.md](update_readme.md) 了解如何同步最新 skill。

当前版本：v2.0.0
