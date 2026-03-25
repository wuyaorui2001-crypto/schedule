#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schedule Config - 集中配置文件
日程管理项目的所有配置常量
"""

from pathlib import Path

# 项目根目录
PROJECT_DIR = Path(__file__).parent.parent

# 年度文件目录（同级目录）
YEAR_FILES_PATH = PROJECT_DIR

# 脚本目录
SCRIPTS_PATH = PROJECT_DIR / "scripts"

# 报表输出目录（暂无）
# REPORTS_PATH = PROJECT_DIR / "reports"

# 状态列表
STATUSES = ["待办", "进行中", "已完成", "取消"]

# 优先级列表（从高到低）
PRIORITIES = ["P0紧急", "P1高", "P2中", "P3低"]

# 分类列表
CATEGORIES = ["工作", "生活", "学习", "健康", "人际", "娱乐"]

# 标签到分类的映射
TAG_CATEGORY_MAP = {
    # 工作
    "工作": "工作",
    "上班": "工作",
    "开会": "工作",
    "报告": "工作",
    "班会": "工作",
    "班级": "工作",
    # 生活
    "生活": "生活",
    "吃饭": "生活",
    "买菜": "生活",
    "取快递": "生活",
    "快递": "生活",
    # 学习
    "学习": "学习",
    "阅读": "学习",
    "课程": "学习",
    "读书": "学习",
    # 健康
    "健康": "健康",
    "运动": "健康",
    "健身": "健康",
    "休息": "健康",
    # 人际
    "人际": "人际",
    "聚会": "人际",
    "聚餐": "人际",
    "社交": "人际",
    # 娱乐
    "娱乐": "娱乐",
    "电影": "娱乐",
    "游戏": "娱乐",
    "旅行": "娱乐",
    # 财务
    "财务": "工作",
    "记账": "工作",
}

# 默认提醒偏移量（分钟）
DEFAULT_REMINDER_OFFSETS = [1440, 60, 10]  # 24h, 1h, 10m

# 时间格式
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
