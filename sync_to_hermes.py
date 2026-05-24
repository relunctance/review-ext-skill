#!/usr/bin/env python3
"""
sync_to_hermes.py - 同步 ext-skill 到 Hermes profile

用法:
    python sync_to_hermes.py <role> [--dry-run] [--force]
    python sync_to_hermes.py arc --dry-run  # 预览，不实际执行

示例:
    python sync_to_hermes.py coder     # 同步 coder-ext-skill
    python sync_to_hermes.py arc --force  # 强制同步

设计原则:
    1. 只同步指定的 role-ext-skill
    2. 不污染其他 profile
    3. 可预览（--dry-run）
    4. 可强制覆盖（--force）
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import Set, List, Dict, Optional


# 常量
# 注意：WSL 环境下 Path.home() 可能返回 ~/.hermes/profiles/<profile>/home
# 所以使用明确的绝对路径
HERMES_BASE = Path("/home/gql/.hermes/profiles")
REPOS_BASE = Path("/home/gql/repos")
GQL_BOTS_SHARED = Path("/home/gql/gql-bots/shared")

# 允许的 role 列表
VALID_ROLES = {"arc", "sm", "coder", "review", "qa", "leader"}

# 参考文档目录下的文件名黑名单（不创建 skill 链接）
SKIP_SKILLS = {"quick-reference"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="同步 ext-skill 到 Hermes profile",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python sync_to_hermes.py coder       # 同步 coder-ext-skill
    python sync_to_hermes.py arc --dry-run  # 预览
    python sync_to_hermes.py sm --force  # 强制覆盖
        """
    )
    parser.add_argument("role", choices=list(VALID_ROLES), help="角色名称")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际执行")
    parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")
    parser.add_argument("--hermes-base", type=Path, default=HERMES_BASE,
                        help=f"Hermes profiles 目录 (默认: {HERMES_BASE})")
    parser.add_argument("--repos-base", type=Path, default=REPOS_BASE,
                        help=f"ext-skill 仓库目录 (默认: {REPOS_BASE})")
    return parser.parse_args()


def get_ext_skill_dir(role: str, repos_base: Path) -> Path:
    """获取 ext-skill 仓库目录"""
    return repos_base / f"{role}-ext-skill"


def get_skill_dir(role: str, hermes_base: Path) -> Path:
    """获取 Hermes profile 的 skills 目录"""
    return hermes_base / role / "skills"


def get_ext_skill_skill_dir(role: str, hermes_base: Path) -> Path:
    """获取 Hermes 下 ext-skill 的目标目录"""
    return hermes_base / role / "skills" / f"{role}-ext-skill"


def validate_environment(repos_base: Path, role: str) -> bool:
    """验证环境是否正确"""
    ext_skill_dir = get_ext_skill_dir(role, repos_base)
    
    if not ext_skill_dir.exists():
        print(f"❌ 错误: ext-skill 仓库不存在: {ext_skill_dir}")
        return False
    
    if not (ext_skill_dir / "SKILL.md").exists():
        print(f"❌ 错误: {ext_skill_dir} 不是有效的 ext-skill（缺少 SKILL.md）")
        return False
    
    return True


def get_reference_skills(ext_skill_dir: Path) -> List[str]:
    """获取需要创建 skill 链接的参考文档列表"""
    references_dir = ext_skill_dir / "references"
    if not references_dir.exists():
        return []
    
    skills = []
    for ref_file in references_dir.glob("*.md"):
        skill_name = ref_file.stem  # 文件名（不含扩展名）
        if skill_name not in SKIP_SKILLS:
            skills.append(skill_name)
    
    return sorted(skills)


def sync_ext_skill(role: str, args) -> Dict[str, any]:
    """
    同步 ext-skill 到 Hermes profile
    
    返回: {
        "success": bool,
        "actions": List[str],
        "errors": List[str]
    }
    """
    result = {"success": True, "actions": [], "errors": []}
    
    repos_base = args.repos_base
    hermes_base = args.hermes_base
    dry_run = args.dry_run
    force = args.force
    
    ext_skill_dir = get_ext_skill_dir(role, repos_base)
    skill_dir = get_skill_dir(role, hermes_base)
    ext_skill_target = get_ext_skill_skill_dir(role, hermes_base)
    
    # 1. 创建目标目录
    action = f"创建目录: {skill_dir}"
    if dry_run:
        result["actions"].append(f"[DRY-RUN] {action}")
    else:
        result["actions"].append(action)
        skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. 复制 ext-skill 到目标目录
    if ext_skill_target.exists() and not force:
        action = f"跳过复制: {ext_skill_target} 已存在（使用 --force 覆盖）"
        result["actions"].append(action)
    else:
        action = f"复制: {ext_skill_dir} → {ext_skill_target}"
        if dry_run:
            result["actions"].append(f"[DRY-RUN] {action}")
        else:
            result["actions"].append(action)
            if ext_skill_target.exists():
                shutil.rmtree(ext_skill_target)
            shutil.copytree(ext_skill_dir, ext_skill_target, symlinks=True)
    
    # 3. 创建 reference skills 的软链接
    reference_skills = get_reference_skills(ext_skill_dir)
    for skill_name in reference_skills:
        skill_target_dir = skill_dir / skill_name
        skill_source = ext_skill_target / "references" / f"{skill_name}.md"
        skill_target_file = skill_target_dir / "SKILL.md"
        
        if skill_target_file.exists() and not force:
            action = f"跳过链接: {skill_name} 已存在"
            result["actions"].append(action)
        else:
            action = f"创建链接: {skill_name} → {skill_source.name}"
            if dry_run:
                result["actions"].append(f"[DRY-RUN] {action}")
            else:
                result["actions"].append(action)
                skill_target_dir.mkdir(parents=True, exist_ok=True)
                if skill_target_file.is_symlink() or skill_target_file.exists():
                    os.remove(skill_target_file)
                os.symlink(skill_source, skill_target_file)
    
    # 4. 创建 shared/ 软链接
    shared_target = ext_skill_target / "shared" / "communication"
    shared_source = GQL_BOTS_SHARED
    
    if shared_source.exists():
        action = f"创建链接: shared/communication → {shared_source}"
        if dry_run:
            result["actions"].append(f"[DRY-RUN] {action}")
        else:
            result["actions"].append(action)
            shared_target.parent.mkdir(parents=True, exist_ok=True)
            if shared_target.is_symlink() or shared_target.exists():
                os.remove(shared_target)
            os.symlink(shared_source, shared_target)
    
    return result


def cleanup_other_ext_skills(role: str, args) -> Dict[str, any]:
    """
    清理其他 ext-skills（防止污染）
    
    只保留当前 role 的 ext-skill，删除其他的
    """
    result = {"success": True, "actions": [], "errors": []}
    
    hermes_base = args.hermes_base
    dry_run = args.dry_run
    skill_dir = get_skill_dir(role, hermes_base)
    
    if not skill_dir.exists():
        return result
    
    # 需要保留的 ext-skill 名称
    keep_ext_skill = f"{role}-ext-skill"
    
    for item in skill_dir.iterdir():
        if not item.is_dir():
            continue
        
        item_name = item.name
        
        # 跳过 gql-* 和非 ext-skill 目录
        if item_name.startswith("gql-"):
            continue
        
        # 检查是否是 ext-skill（以 -ext-skill 结尾）
        if item_name.endswith("-ext-skill"):
            if item_name != keep_ext_skill:
                action = f"清理（污染）: {item_name}"
                if dry_run:
                    result["actions"].append(f"[DRY-RUN] {action}")
                else:
                    result["actions"].append(action)
                    try:
                        shutil.rmtree(item)
                    except Exception as e:
                        result["errors"].append(f"删除 {item_name} 失败: {e}")
            else:
                result["actions"].append(f"保留: {item_name}")
    
    return result


def print_result(result: Dict[str, any]):
    """打印执行结果"""
    print("\n" + "=" * 50)
    print("执行的操作:")
    for action in result["actions"]:
        print(f"  {action}")
    
    if result["errors"]:
        print("\n错误:")
        for error in result["errors"]:
            print(f"  ❌ {error}")
        print("\n❌ 同步失败")
    else:
        print("\n✅ 同步成功")


def main():
    args = parse_args()
    role = args.role
    
    print(f"=== 同步 {role}-ext-skill 到 Hermes ===")
    print(f"Hermes base: {args.hermes_base}")
    print(f"Repos base: {args.repos_base}")
    if args.dry_run:
        print("⚠️  DRY-RUN 模式（不实际执行）")
    print()
    
    # 1. 验证环境
    if not validate_environment(args.repos_base, role):
        sys.exit(1)
    
    # 2. 清理其他 ext-skills（防止污染）
    print("--- 清理污染的 ext-skills ---")
    cleanup_result = cleanup_other_ext_skills(role, args)
    print_result(cleanup_result)
    
    # 3. 同步当前 ext-skill
    print("\n--- 同步 ext-skill ---")
    sync_result = sync_ext_skill(role, args)
    print_result(sync_result)
    
    # 4. 汇总结果
    all_success = cleanup_result["success"] and sync_result["success"]
    all_errors = cleanup_result["errors"] + sync_result["errors"]
    
    if all_errors:
        for error in all_errors:
            print(f"❌ {error}")
        sys.exit(1)
    
    print(f"\n✅ 同步完成: {role}-ext-skill")
    
    # 5. 列出最终状态
    print("\n--- 最终状态 ---")
    skill_dir = get_skill_dir(role, args.hermes_base)
    if skill_dir.exists():
        for item in sorted(skill_dir.iterdir()):
            print(f"  {item.name}")


if __name__ == "__main__":
    main()
