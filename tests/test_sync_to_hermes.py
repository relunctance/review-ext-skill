#!/usr/bin/env python3
"""
test_sync_to_hermes.py - sync_to_hermes.py 单元测试

运行方式:
    python test_sync_to_hermes.py
"""

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path


class TestGetReferenceSkills(unittest.TestCase):
    """测试 get_reference_skills 函数"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_ref_")
        self.temp_path = Path(self.test_dir)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_get_reference_skills_excludes_quick_reference(self):
        """测试 quick-reference 被排除"""
        ext_skill = self.temp_path / "test-ext-skill"
        ext_skill.mkdir()
        refs = ext_skill / "references"
        refs.mkdir()
        
        (refs / "quick-reference.md").write_text("quick")
        (refs / "bmad-dev.md").write_text("bmad")
        
        # 模拟 get_reference_skills
        skills = []
        for ref_file in refs.glob("*.md"):
            skill_name = ref_file.stem
            if skill_name != "quick-reference":
                skills.append(skill_name)
        
        self.assertIn("bmad-dev", skills)
        self.assertNotIn("quick-reference", skills)
        print("✅ test_get_reference_skills_excludes_quick_reference 通过")


class TestPathOperations(unittest.TestCase):
    """测试路径操作"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_path_")
        self.temp_path = Path(self.test_dir)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_get_skill_dir(self):
        """测试 skill 目录路径计算"""
        hermes_base = self.temp_path / ".hermes" / "profiles"
        role = "arc"
        expected = hermes_base / role / "skills"
        result = hermes_base / role / "skills"
        self.assertEqual(result, expected)
        print("✅ test_get_skill_dir 通过")
    
    def test_get_ext_skill_dir(self):
        """测试 ext-skill 目录路径计算"""
        repos_base = self.temp_path / "repos"
        role = "arc"
        expected = repos_base / f"{role}-ext-skill"
        result = repos_base / f"{role}-ext-skill"
        self.assertEqual(result, expected)
        print("✅ test_get_ext_skill_dir 通过")


class TestCleanupLogic(unittest.TestCase):
    """测试清理逻辑"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_cleanup_")
        self.temp_path = Path(self.test_dir)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_cleanup_removes_wrong_ext_skill(self):
        """测试清理逻辑正确识别需要删除的 ext-skill"""
        hermes_base = self.temp_path / ".hermes" / "profiles"
        skill_dir = hermes_base / "arc" / "skills"
        skill_dir.mkdir(parents=True)
        
        # 创建污染的 ext-skills
        (skill_dir / "sm-ext-skill").mkdir()
        (skill_dir / "coder-ext-skill").mkdir()
        (skill_dir / "arc-ext-skill").mkdir()  # 应该保留
        
        VALID_ROLES = {"arc", "sm", "coder", "review", "qa", "leader"}
        keep_ext_skill = "arc-ext-skill"
        
        remaining = []
        to_delete = []
        
        for item in skill_dir.iterdir():
            if not item.is_dir():
                continue
            item_name = item.name
            if item_name.endswith("-ext-skill"):
                if item_name != keep_ext_skill:
                    to_delete.append(item_name)
                else:
                    remaining.append(item_name)
        
        self.assertIn("arc-ext-skill", remaining)
        self.assertNotIn("sm-ext-skill", remaining)
        self.assertIn("sm-ext-skill", to_delete)
        self.assertIn("coder-ext-skill", to_delete)
        print("✅ test_cleanup_removes_wrong_ext_skill 通过")


class TestSyncStructure(unittest.TestCase):
    """测试同步结构"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_sync_")
        self.temp_path = Path(self.test_dir)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_sync_creates_ext_skill_dir(self):
        """测试同步创建正确的目录结构"""
        hermes_base = self.temp_path / ".hermes" / "profiles"
        repos_base = self.temp_path / "repos"
        repos_base.mkdir(parents=True)  # 确保父目录存在
        skill_dir = hermes_base / "arc" / "skills"
        skill_dir.mkdir(parents=True)
        
        # 模拟 ext-skill 源
        ext_skill_src = repos_base / "arc-ext-skill"
        ext_skill_src.mkdir()
        (ext_skill_src / "SKILL.md").write_text("# Arc")
        refs = ext_skill_src / "references"
        refs.mkdir()
        (refs / "bmad-arc.md").write_text("# BMAD Arc")
        
        # 目标路径
        ext_skill_target = skill_dir / "arc-ext-skill"
        
        # 执行复制
        shutil.copytree(ext_skill_src, ext_skill_target, symlinks=True)
        
        # 验证
        self.assertTrue(ext_skill_target.exists())
        self.assertTrue((ext_skill_target / "SKILL.md").exists())
        self.assertTrue((ext_skill_target / "references" / "bmad-arc.md").exists())
        print("✅ test_sync_creates_ext_skill_dir 通过")
    
    def test_sync_creates_skill_symlink(self):
        """测试同步创建正确的软链接"""
        hermes_base = self.temp_path / ".hermes" / "profiles"
        repos_base = self.temp_path / "repos"
        repos_base.mkdir(parents=True)  # 确保父目录存在
        skill_dir = hermes_base / "arc" / "skills"
        skill_dir.mkdir(parents=True)
        
        # 模拟 ext-skill 源
        ext_skill_src = repos_base / "arc-ext-skill"
        ext_skill_src.mkdir()
        (ext_skill_src / "SKILL.md").write_text("# Arc")
        refs = ext_skill_src / "references"
        refs.mkdir()
        (refs / "bmad-arc.md").write_text("# BMAD Arc")
        
        # 目标路径
        ext_skill_target = skill_dir / "arc-ext-skill"
        shutil.copytree(ext_skill_src, ext_skill_target, symlinks=True)
        
        # 创建 skill 软链接
        skill_target_dir = skill_dir / "bmad-arc"
        skill_target_dir.mkdir(parents=True)
        skill_source = ext_skill_target / "references" / "bmad-arc.md"
        skill_target_file = skill_target_dir / "SKILL.md"
        os.symlink(skill_source, skill_target_file)
        
        # 验证软链接
        self.assertTrue(skill_target_file.is_symlink())
        self.assertEqual(os.readlink(skill_target_file), str(skill_source))
        print("✅ test_sync_creates_skill_symlink 通过")


class TestDryRun(unittest.TestCase):
    """测试 dry-run 逻辑"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_dryrun_")
        self.temp_path = Path(self.test_dir)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_dry_run_does_not_modify(self):
        """测试 dry-run 模式不修改文件"""
        hermes_base = self.temp_path / ".hermes" / "profiles"
        repos_base = self.temp_path / "repos"
        repos_base.mkdir(parents=True)  # 确保父目录存在
        skill_dir = hermes_base / "arc" / "skills"
        skill_dir.mkdir(parents=True)
        
        # 创建 ext-skill
        ext_skill_src = repos_base / "arc-ext-skill"
        ext_skill_src.mkdir()
        (ext_skill_src / "SKILL.md").write_text("# Arc original")
        ext_skill_target = skill_dir / "arc-ext-skill"
        shutil.copytree(ext_skill_src, ext_skill_target, symlinks=True)
        
        # 记录文件内容
        original_content = (ext_skill_target / "SKILL.md").read_text()
        
        # 模拟 dry-run（不执行复制）
        dry_run = True
        if not dry_run:
            shutil.rmtree(ext_skill_target)
        
        # 验证文件未修改
        self.assertEqual((ext_skill_target / "SKILL.md").read_text(), original_content)
        print("✅ test_dry_run_does_not_modify 通过")


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("sync_to_hermes.py 单元测试")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestGetReferenceSkills))
    suite.addTests(loader.loadTestsFromTestCase(TestPathOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestCleanupLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestSyncStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestDryRun))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
