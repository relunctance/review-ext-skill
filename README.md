# Review Ext Skill

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/platforms-hermes-blue.svg)](#)
[![Version](https://img.shields.io/badge/Version-2.0.0-green.svg)](SKILL.md)
[![Review Skills](https://img.shields.io/badge/Review_Skills-7-orange.svg)](#)
[![Auto Route](https://img.shields.io/badge/Auto_Route-Enabled-blue.svg)](#)

代码评审技能索引路由器 - 接收任何评审任务，智能推荐最合适的 skill 并执行。

## 一句话路由规则

```
收到评审任务
    │
    ├─ "评审"/"pr" → bmad-review
    ├─ "安全"/"漏洞" → frontend/backend-security-coder
    ├─ "架构" → architect-review
    └─ 无匹配 → bmad-review
```

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
| architect-review | 架构评审 | P1 |
| security-auditor | 安全审计 | P2 |

## 同步到 Hermes

### 安装 Skill 文件到 Hermes Profile

```bash
# 进入仓库目录
cd /home/gql/repos/review-ext-skill

# 执行同步脚本
bash sync-to-hermes.sh review
```

同步后目录结构：
```
~/.hermes/profiles/review/skills/
├── review-ext-skill/                    # 路由器
│   ├── SKILL.md
│   └── references/
├── bmad-review/                       # 独立 skill（软链接）
│   └── SKILL.md → review-ext-skill/references/bmad-review.md
├── code-reviewer/                     # 独立 skill（软链接）
│   └── SKILL.md → review-ext-skill/references/code-reviewer.md
└── ...                               # 其他 skills
```

### 验证安装

```bash
# 查看已安装的 skills
ls -la ~/.hermes/profiles/review/skills/

# 验证软链接
readlink -f ~/.hermes/profiles/review/skills/bmad-review/SKILL.md
```

---

## 工作流

详见 [SKILL.md](SKILL.md)

## 升级

详见 [update_readme.md](update_readme.md)
