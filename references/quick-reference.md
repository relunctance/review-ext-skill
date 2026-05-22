<!-- TL;DR: 自然语言示例 + Fallback + 组合流快速参考 -->

# Review 技能路由快速参考

> 详细决策树见 SKILL.md 主文件

## 🗣️ 自然语言触发示例

| 用户实际说法 | → 路由到 | 说明 |
|-------------|---------|------|
| "评审这个 PR" | bmad-review | 评审核心 |
| "检查代码质量" | code-reviewer | 代码风格 |
| "前端安全检查" | frontend-security-coder | XSS/CSRF |
| "后端安全检查" | backend-security-coder | SQL注入 |
| "处理评审意见" | receiving-code-review | 反馈处理 |
| "架构合理性" | architect-review | 设计原则 |
| "全面安全审计" | security-auditor | OWASP |

---

## 🔄 Fallback 处理

当任务**无法匹配**时：

```
无匹配 → bmad-review（让评审核心帮你判断）
```

---

## 🔗 任务组合流

### 组合 1: 完整代码评审

```
"完整评审 PR"
    └─ bmad-review
          ├─ code-reviewer（质量）
          ├─ frontend-security-coder（前端）
          ├─ backend-security-coder（后端）
          └─ architect-review（如需）
```

### 组合 2: 安全专项评审

```
"检查安全漏洞"
    ├─ frontend-security-coder
    ├─ backend-security-coder
    └─ security-auditor（全面）
```

### 组合 3: 反馈处理

```
"处理评审意见"
    └─ receiving-code-review
```

---

## ⚡ 快速决策速查卡

```
┌─────────────────────────────────────────────────────────────┐
│  场景              │  首选 Skill           │  组合        │
├─────────────────────────────────────────────────────────────┤
│  PR/代码评审        │  bmad-review         │  →code-rev  │
│  代码质量          │  code-reviewer       │              │
│  前端安全          │  frontend-sec-coder  │              │
│  后端安全          │  backend-sec-coder   │              │
│  架构评审          │  architect-review    │              │
│  处理反馈          │  receiving-code-rev  │              │
│  全面安全审计       │  security-auditor   │              │
│  未知              │  bmad-review        │  询问澄清    │
└─────────────────────────────────────────────────────────────┘
```
