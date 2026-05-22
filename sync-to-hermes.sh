#!/bin/bash
# sync-to-hermes.sh - 同步 ext-skill 到 Hermes profile
# 用法: ./sync-to-hermes.sh [role]
# 示例: ./sync-to-hermes.sh qa

ROLE=${1:-qa}
SKILL_DIR=/home/gql/.hermes/profiles/${ROLE}/skills
EXT_SKILL_DIR=${SKILL_DIR}/${ROLE}-ext-skill

echo "=== 同步 ${ROLE}-ext-skill 到 Hermes ==="

# 1. 复制 ext-skill 到 profile skills 目录
cp -rf /home/gql/repos/${ROLE}-ext-skill ${EXT_SKILL_DIR}
echo "✓ 复制 ${ROLE}-ext-skill 到 ${EXT_SKILL_DIR}"

# 2. 对每个 reference skill，创建独立的 skill 目录 + 软链接
for ref_file in ${EXT_SKILL_DIR}/references/*.md; do
  skillname=$(basename "$ref_file" .md)
  
  # 跳过 quick-reference.md
  if [[ "$skillname" == "quick-reference" ]]; then
    echo "⏭ 跳过 quick-reference.md"
    continue
  fi
  
  # 创建 skill 目录并链接
  mkdir -p ${SKILL_DIR}/${skillname}
  ln -sf ${EXT_SKILL_DIR}/references/${skillname}.md ${SKILL_DIR}/${skillname}/SKILL.md
  
  echo "✓ ${skillname}"
done


# 3. 创建 shared/ 软链接（指向 gql-bots/shared/）
mkdir -p ${EXT_SKILL_DIR}/shared
ln -sf /home/gql/gql-bots/shared/communication ${EXT_SKILL_DIR}/shared/communication
echo "✓ shared/communication → /home/gql/gql-bots/shared/communication"

echo ""
echo "=== 同步完成 ==="
ls -la ${SKILL_DIR}/
