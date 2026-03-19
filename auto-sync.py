#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schedule 自动同步脚本
支持双模式：定期同步（每周日）+ 手动同步（用户指令）
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

# 设置环境变量避免编码问题
os.environ['PYTHONIOENCODING'] = 'utf-8'

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def sync_to_github():
    """同步到GitHub"""
    project_dir = Path(__file__).parent
    
    print("[INFO] 开始同步 Schedule 到 GitHub...")
    
    # 1. 检查是否有更改
    print("[INFO] 检查Git状态...")
    success, stdout, stderr = run_command("git status --porcelain", cwd=project_dir)
    if not success:
        print(f"[ERROR] Git状态检查失败")
        return False
    
    if not stdout.strip():
        print("[INFO] 没有需要同步的更改")
        return True
    
    # 2. 添加所有更改
    print("[INFO] 添加更改到Git...")
    success, _, stderr = run_command("git add .", cwd=project_dir)
    if not success:
        print(f"[ERROR] Git add 失败")
        return False
    
    # 3. 提交
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"自动同步: 更新日程记录 @ {timestamp}"
    print(f"[INFO] 提交更改...")
    success, _, stderr = run_command(f'git commit -m "{commit_msg}"', cwd=project_dir)
    if not success:
        print(f"[ERROR] Git commit 失败")
        return False
    
    # 4. 推送到GitHub（先尝试main，失败则尝试master）
    print("[INFO] 推送到GitHub...")
    success, stdout, stderr = run_command("git push origin main", cwd=project_dir)
    if not success:
        print("[WARN] main分支推送失败，尝试master分支...")
        success, stdout, stderr = run_command("git push origin master", cwd=project_dir)
        if not success:
            print(f"[ERROR] Git push 失败（main和master都失败）")
            return False
    
    print("[OK] 同步完成!")
    print(f"[INFO] 数据已备份到GitHub")
    return True

if __name__ == "__main__":
    success = sync_to_github()
    sys.exit(0 if success else 1)
