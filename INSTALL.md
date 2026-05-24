# INSTALL.md - Review Ext Skill 安装部署

## 前置要求

- Hermes Agent 已安装
- 目标 profile 已存在（如 `review`）

## 安装步骤

### 方式 1：使用同步脚本（推荐）

```bash
# 进入仓库目录
cd /home/gql/repos/review-ext-skill

# 执行同步脚本
python sync_to_hermes.py review
```

### 方式 2：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/relunctance/review-ext-skill.git ~/.hermes/profiles/review/skills/review-ext-skill

# 2. 进入目录
cd ~/.hermes/profiles/review/skills/review-ext-skill

# 3. 执行同步
python sync_to_hermes.py review
```

## 验证安装

```bash
# 查看已安装的 skills
ls -la ~/.hermes/profiles/review/skills/

# 验证软链接
readlink -f ~/.hermes/profiles/review/skills/review-ext-skill/SKILL.md
```

## 目录结构

安装后 `~/.hermes/profiles/review/skills/` 应包含：

```
review/
├── review-ext-skill/           # 主 skill
│   ├── SKILL.md
│   ├── AGENTS.md
│   ├── INSTALL.md
│   ├── references/
│   └── shared/
├── gql-review/                 # 主角色 skill（来自 gql-bots）
└── ...
```

## 配置文件

### vars.md 配置

`review/vars.md` 应包含：

```yaml
# Review 配置变量
DOCS_HOME: {{GQL_BOTS_HOME}}/docs

## 通知模式
notify_mode: team  # report | team
HERMES_PROFILE: review
FEISHU_MAIN: oc_22e019265c6096916f5a78de44f3cdea

## 模式配置
MODE_CONFIG: full_auto  # full_auto | semi_auto
```

## 更新 skill

```bash
cd /home/gql/repos/review-ext-skill
git pull
python sync_to_hermes.py review
```

## 卸载

```bash
rm -rf ~/.hermes/profiles/review/skills/review-ext-skill
```
