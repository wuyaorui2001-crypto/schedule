# SYSTEM - 日程管理 AI操作指南

> 本文件是AI接手日程项目的必读指南
> 版本: v3.0 | 更新: 2026-03-19
> **基于 reminder skill 优化，使用 Telegram 提醒**

---

## 1. 项目一句话定义

**个人日程与任务管理系统，基于 reminder skill，支持自然语言输入、自动 Telegram 提醒、待办追踪。**

---

## 2. 核心架构

### 依赖 Skill
- **reminder** (已安装) - 自然语言解析 + Telegram 提醒

### 数据存储
- **Events 文件**: `~/.openclaw/workspace/reminders/events.yml`
- **模板**: `~/.openclaw/workspace/skills/reminder/assets/events.template.yml`

### 提醒方式
- **渠道**: Telegram
- **默认提醒时间**: 24h / 1h / 10m 前
- **配置**: `REMINDER_TZ=Asia/Shanghai`, `REMINDER_OFFSETS_MINUTES=1440,60,10`

---

## 3. AI接手后的标准SOP流程

### 场景A：自然语言添加日程

**用户输入示例：**
- "后天上午10点开会"
- "下个月2号我妈生日"
- "周五下午三点交报告"

**处理流程：**
1. **解析事件** (由 reminder skill 处理):
   - title: 事件标题
   - start datetime: 开始时间 (上海时区)
   - notes: 备注 (可选)
   - reminders offsets: 提醒偏移量 (默认 24h/1h/10m)
   - repeat: 重复规则 (可选: yearly/monthly/weekly)

2. **信息不明确时询问** (最小化问题):
   - "后天" 具体日期？
   - "下个月" 是哪个月？
   - 农历生日转换？
   - 时间缺失？

3. **存储记录**:
   - 写入 `reminders/events.yml`

4. **设置提醒**:
   - 使用 `cron` 创建定时任务
   - 提醒发送到当前 Telegram 对话

### 场景B：查看待办/日程

**用户输入：**
- "我最近有什么安排？"
- "下周有什么？"
- "查看待办"

**处理流程：**
1. 读取 `reminders/events.yml`
2. 计算即将到来的事项 (上海时间)
3. 分类展示：
   ```
   [⏰ 即将到来]
   1. 明天 10:00 开会
   2. 后天 15:00 交报告
   
   [📅 本周安排]
   1. 周五 18:00 聚餐
   ```

### 场景C：完成/取消待办

**处理流程：**
1. 找到对应事件
2. 更新状态或删除
3. 移除相关的 cron 任务
4. 确认变更

---

## 4. 数据格式 (reminder skill 标准)

### Events.yml 格式
```yaml
events:
  - id: "uuid"
    title: "开会"
    start: "2026-03-21T10:00:00+08:00"
    timezone: "Asia/Shanghai"
    reminders:
      - minutes: 1440  # 24h
      - minutes: 60    # 1h
      - minutes: 10    # 10m
    repeat: null  # yearly/monthly/weekly
    notes: "项目进度汇报"
    created_at: "2026-03-19T15:00:00+08:00"
```

### 自然语言解析规则

| 输入 | 解析结果 |
|-----|---------|
| 今天 | 2026-03-19 |
| 明天 | 2026-03-20 |
| 后天 | 2026-03-21 |
| 下周三 | 下周的周三 |
| 下个月2号 | 下个月2号 |
| 上午10点 | 10:00 |
| 下午3点 | 15:00 |
| 晚上8点 | 20:00 |

### 重复规则

| 输入 | 解析结果 |
|-----|---------|
| 每天 | repeat: daily |
| 每周五 | repeat: weekly |
| 每月1号 | repeat: monthly |
| 每年 | repeat: yearly |

---

## 5. 常见场景处理示例

### 示例1：添加日程
```
用户：后天上午10点开会
AI：确认添加：2026-03-21 10:00 开会，设置提醒 24h/1h/10m 前？
用户：是的
AI：已添加，将在 Telegram 提醒你。
```

### 示例2：查看安排
```
用户：最近有什么安排？
AI：
[即将到来]
1. 明天 10:00 开会
2. 后天 15:00 交报告
```

### 示例3：农历生日
```
用户：农历三月初五是我妈生日
AI：农历三月初五对应的公历是 2026-04-22，是否每年重复？
用户：是的
AI：已添加：每年农历三月初五（公历 2026-04-22）妈妈生日
```

---

## 6. 与旧版 Schedule 的区别

| 功能 | 旧版 (v2.0) | 新版 (v3.0) |
|------|------------|------------|
| 数据存储 | `schedule/YYYY-MM.md` | `reminders/events.yml` |
| 提醒方式 | 飞书 | **Telegram** |
| 自然语言 | 自定义解析 | **reminder skill** |
| 重复任务 | 手动设置 | **自动支持** |
| 跨设备同步 | Git | **Git + claw-roam** |

---

## 7. GitHub 集成

### 仓库地址
- **日程管理**: https://github.com/wuyaorui2001-crypto/schedule

### 数据同步
- `reminders/events.yml` 纳入 Git 版本控制
- 支持跨设备同步

---

## 8. 可迁移性说明

**符合 agent-workspace PATTERN-005 标准**

新Agent读取本文件后应能：
- 理解基于 reminder skill 的工作流程
- 掌握 Telegram 提醒机制
- 知道数据存储位置
- 无需用户解释即可开始工作

---

*最后更新：2026-03-19*
*基于 reminder skill v0.1.1*
