#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schedule Recalc - 自动计算统计数据
读取年度文件，根据日程明细计算各项统计

支持 --dry-run 参数（只输出不写入）
支持 --update 参数（实际更新文件中的统计面板）
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# 导入统一解析模块
sys.path.insert(0, str(Path(__file__).parent))
from parser import parse_year_file, get_current_year, get_or_default_year_file, STATUSES, PRIORITIES


def calculate_monthly_stats(records: List[Dict[str, Any]], year: int, month: str) -> Dict[str, Any]:
    """计算指定月份的统计数据"""
    month_records = [r for r in records if r['year'] == str(year) and r['month'] == month]

    # 按状态统计
    by_status = {s: 0 for s in STATUSES}
    for r in month_records:
        status = r.get('status', '待办')
        if status in by_status:
            by_status[status] += 1

    # 高优先级统计
    high_priority = len([r for r in month_records if r.get('priority') in ['P0紧急', 'P1高']])

    # 按时长统计（有时间的 vs 无时间的）
    with_time = len([r for r in month_records if r.get('time')])
    without_time = len([r for r in month_records if not r.get('time')])

    return {
        'month': month,
        'total': len(month_records),
        'by_status': by_status,
        'completed': by_status.get('已完成', 0),
        'pending': by_status.get('待办', 0),
        'in_progress': by_status.get('进行中', 0),
        'cancelled': by_status.get('取消', 0),
        'high_priority': high_priority,
        'with_time': with_time,
        'without_time': without_time,
    }


def calculate_year_stats(records: List[Dict[str, Any]], year: int) -> Dict[str, Any]:
    """计算年度统计数据"""
    year_records = [r for r in records if r['year'] == str(year)]

    # 按状态统计
    by_status = {s: 0 for s in STATUSES}
    for r in year_records:
        status = r.get('status', '待办')
        if status in by_status:
            by_status[status] += 1

    # 高优先级统计
    high_priority = len([r for r in year_records if r.get('priority') in ['P0紧急', 'P1高']])

    # 月度统计
    monthly_stats = {}
    for month in [f"{i:02d}" for i in range(1, 13)]:
        month_data = calculate_monthly_stats(records, year, month)
        if month_data['total'] > 0:
            monthly_stats[month] = month_data

    return {
        'year': year,
        'total': len(year_records),
        'by_status': by_status,
        'completed': by_status.get('已完成', 0),
        'pending': by_status.get('待办', 0),
        'in_progress': by_status.get('进行中', 0),
        'cancelled': by_status.get('取消', 0),
        'high_priority': high_priority,
        'monthly_stats': monthly_stats,
    }


def format_stats_output(stats: Dict[str, Any], stats_type: str = 'monthly') -> str:
    """格式化统计输出"""
    output = []

    if stats_type == 'monthly':
        month = stats['month']
        output.append(f"\n[ {month} 月数据面板 ]")
        output.append(f"  总任务: {stats['total']}")
        output.append(f"  已完成: {stats['completed']}")
        output.append(f"  待办: {stats['pending']}")
        output.append(f"  进行中: {stats['in_progress']}")
        output.append(f"  取消: {stats['cancelled']}")
        output.append(f"  高优先级: {stats['high_priority']}")

    elif stats_type == 'yearly':
        year = stats['year']
        output.append(f"\n[ {year} 年度总览 ]")
        output.append(f"  总任务数: {stats['total']}")
        output.append(f"  已完成: {stats['completed']}")
        output.append(f"  待办: {stats['pending']}")
        output.append(f"  进行中: {stats['in_progress']}")
        output.append(f"  取消: {stats['cancelled']}")
        output.append(f"  高优先级: {stats['high_priority']}")

    return '\n'.join(output)


def recalc_year(year: Optional[int] = None, dry_run: bool = True, update: bool = False) -> Dict[str, Any]:
    """
    计算指定年份的统计数据

    参数:
        year: 年份，默认当前年份
        dry_run: True=只输出不写入，False=实际更新
        update: True=实际更新文件

    返回:
        年度统计数据
    """
    filepath, year = get_or_default_year_file(year)

    print(f"[INFO] 读取年度文件: {filepath}")

    # 解析文件
    records = parse_year_file(filepath)
    print(f"[INFO] 找到 {len(records)} 条记录")

    if not records:
        print(f"[WARN] 没有找到记录")
        return {}

    # 计算年度统计
    year_stats = calculate_year_stats(records, year)
    monthly_stats = year_stats.get('monthly_stats', {})

    # 输出年度总览
    print(format_stats_output(year_stats, 'yearly'))

    # 输出各月统计（只显示有数据的月份）
    for month, m_stats in sorted(monthly_stats.items()):
        print(format_stats_output(m_stats, 'monthly'))

    if dry_run:
        print(f"\n[INFO] --dry-run 模式：只输出，不写入文件")

    return year_stats


def main():
    dry_run = '--dry-run' in sys.argv
    update = '--update' in sys.argv

    # 确定年份
    year = None
    for arg in sys.argv[1:]:
        if arg.isdigit() and len(arg) == 4:
            year = int(arg)

    if year:
        print(f"[INFO] 指定年份: {year}")
    else:
        year = get_current_year()
        print(f"[INFO] 使用当前年份: {year}")

    print(f"[INFO] 模式: {'dry-run' if dry_run else ('update' if update else 'normal')}")

    # 执行统计
    recalc_year(year=year, dry_run=dry_run, update=update)


if __name__ == '__main__':
    main()
