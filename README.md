# Schedule - 日程管理系统

> 个人日程与任务管理，支持自然语言输入、待办追踪、提醒通知

---

## 🔗 GitHub 仓库

| 项目 | 地址 | 说明 |
|-----|------|------|
| **日程管理** | https://github.com/wuyaorui2001-crypto/schedule | 日程数据与配置 |
| **核心资产库** | https://github.com/wuyaorui2001-crypto/agentworkspace | 规则、技能、记忆 |

### 恢复方法
```bash
# 克隆仓库
git clone https://github.com/wuyaorui2001-crypto/schedule.git
cd schedule

# 读取 SYSTEM.md 理解使用规则
cat SYSTEM.md

# 开始管理日程
```

---

## 📋 项目结构

```
schedule/
├── README.md          # 本文件
├── SYSTEM.md          # AI操作指南（必读）
├── MEMORY.md          # 项目复盘记录
├── .learnings/        # 自动学习记录
├── 2026.md           # 2026年日程数据
└── scripts/           # 工具脚本
    ├── auto-sync.py   # 自动同步GitHub
    └── validate.py    # 格式校验
```

---

## ✨ 核心功能

### 自然语言输入
- "后天上午10点开会"
- "下周三下午3点交报告"
- "每月1号还信用卡"

### 待办管理
- 添加待办
- 标记完成 [x]
- 删除待办
- 查看列表

### 提醒通知
- 默认提醒：24h/1h/10m 前
- 支持重复任务
- 可查询近期安排

---

## 📝 数据格式

```markdown
- 2026-03-18 14:00 | [待办] | [P1高] | 会议 | #工作 | 提醒:15分钟前
- 2026-03-19 10:00 | [已完成] | [P0紧急] | 报告 | #工作 | 完成:2026-03-19 09:30
```

---

## 🚀 使用方法

与 AI 对话：
- "添加日程：明天下午2点开会"
- "查看待办"
- "完成第1个"
- "最近有什么安排"

---

*创建于: 2025-03-18 | 优化于: 2026-03-18*
*参考: todo-manager + reminder Skill*
