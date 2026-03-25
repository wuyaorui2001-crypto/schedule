#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schedule Parser - 统一解析模块
提供标准接口解析日程记录
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from config import YEAR_FILES_PATH


# 状态和优先级
STATUSES = ["待办", "进行中", "已完成", "取消"]
PRIORITIES = ["P0紧急", "P1高", "P2中", "P3低"]

# 日程记录正则（简化格式）
# - 2026-03-18 18:00 | [待办] | [P1高] | 吃饭 | #生活
# - 2026-03-18 | [已完成] | [P2中] | 吃饭 | #生活 | 完成:2026-03-18 18:30
RECORD_PATTERN = re.compile(
    r'^-\s*(\d{4}-\d{2}-\d{2})'  # 日期
    r'(?:\s+(\d{2}:\d{2}))?'       # 可选时间
    r'\s*\|\s*\[([^]]+)\]'         # 状态
    r'\s*\|\s*\[([^]]+)\]'         # 优先级
    r'\s*\|\s*([^|]+)'             # 标题
    r'(?:\s*\|\s*(.+))?$'          # 可选标签/备注
)


def parse_record(line: str) -> Optional[Dict[str, Any]]:
    """
    解析单条日程记录

    参数:
        line: 日程行，如 "- 2026-03-18 18:00 | [待办] | [P1高] | 吃饭 | #生活"

    返回:
        解析成功返回字典，包含字段: date, time, status, priority, title, tag, notes
        解析失败返回 None
    """
    line = line.strip()
    if not line.startswith('- '):
        return None

    match = RECORD_PATTERN.match(line)
    if not match:
        return None

    date_str, time_str, status, priority, title, extra = match.groups()

    result = {
        'date': date_str,
        'time': time_str or None,
        'status': status,
        'priority': priority,
        'title': title.strip(),
        'year': date_str[:4],
        'month': date_str[5:7],
        'day': date_str[8:10],
    }

    # 解析额外信息（标签/备注）
    if extra:
        extra = extra.strip()
        if extra.startswith('#'):
            # 格式: #标签 | 备注
            parts = extra.split('|', 1)
            result['tag'] = parts[0].strip()
            result['notes'] = parts[1].strip() if len(parts) > 1 else None
        else:
            result['notes'] = extra

    return result


def parse_year_file(filepath: Path) -> List[Dict[str, Any]]:
    """
    解析年度文件，返回所有记录列表

    参数:
        filepath: 年度文件路径，如 Path("2026.md")

    返回:
        记录字典列表
    """
    records = []

    if not filepath.exists():
        return records

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            record = parse_record(line)
            if record:
                records.append(record)

    return records


def get_current_year() -> int:
    """
    获取当前年份（基于实际日期）

    返回:
        当前年份整数，如 2026
    """
    return datetime.now().year


def get_or_default_year_file(year: Optional[int] = None) -> tuple:
    """
    获取指定年份的文件路径，不存在则返回当前年份

    参数:
        year: 年份整数，如 2026。None 则使用当前年份。

    返回:
        tuple[Path, int]: (文件路径, 实际年份)
    """
    if year is None:
        year = get_current_year()
    return YEAR_FILES_PATH / f"{year}.md", year


def filter_by_status(records: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """筛选指定状态的记录"""
    return [r for r in records if r.get('status') == status]


def filter_by_month(records: List[Dict[str, Any]], year: int, month: str) -> List[Dict[str, Any]]:
    """筛选指定月份的记录"""
    return [r for r in records if r['year'] == str(year) and r['month'] == month]


def get_upcoming(records: List[Dict[str, Any]], days: int = 7) -> List[Dict[str, Any]]:
    """获取即将到来的日程（未来N天内）"""
    today = datetime.now().date()
    upcoming = []

    for r in records:
        if r['status'] == '已完成' or r['status'] == '取消':
            continue
        try:
            record_date = datetime.strptime(r['date'], '%Y-%m-%d').date()
            if 0 <= (record_date - today).days <= days:
                upcoming.append(r)
        except ValueError:
            continue

    return sorted(upcoming, key=lambda x: x['date'])
