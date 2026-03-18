#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日程数据格式校验脚本
"""

import re
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_FILE = PROJECT_DIR / "2026.md"

def validate_schedule(filepath):
    """校验日程文件格式"""
    if not filepath.exists():
        print(f"[ERROR] 文件不存在: {filepath}")
        return False
    
    content = filepath.read_text(encoding='utf-8')
    
    # 匹配记录格式
    pattern = r'- (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| \[(.+?)\] \| \[(.+?)\] \| (.+?) \| #(.+?)(?: \| (.+))?'
    
    records = []
    errors = []
    
    for i, line in enumerate(content.split('\n'), 1):
        if line.startswith('- '):
            match = re.match(pattern, line)
            if not match:
                errors.append(f"第{i}行格式错误: {line[:50]}")
            else:
                records.append(match.groups())
    
    # 报告
    print(f"[INFO] 校验文件: {filepath}")
    print(f"[INFO] 记录数: {len(records)}")
    
    if errors:
        print(f"[ERROR] 发现 {len(errors)} 个错误:")
        for err in errors[:5]:
            print(f"  - {err}")
        return False
    else:
        print("[OK] 格式校验通过")
        return True

if __name__ == '__main__':
    success = validate_schedule(DATA_FILE)
    sys.exit(0 if success else 1)
