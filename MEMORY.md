# MEMORY - 日程管理项目复盘

## 2026-03-25 | v4.0 优化

**背景**: 5年支持 + 无缝继承 + 无缝迁移

**执行内容**：
1. 移除 reminder skill（不再使用）
2. 创建 scripts/parser.py - 统一解析模块
3. 创建 scripts/config.py - 集中配置
4. 创建 scripts/recalc.py - 自动统计计算
5. 重写 SYSTEM.md - 更新 SOP，移除 reminder 引用
6. 提醒改用 cc-connect（Telegram）

**关键决策**：
- reminder skill 去掉（用户确认不用）
- 数据保留在 2026.md（8条记录）
- 提醒通过 cc-connect（已有基础设施）

**通用规则沉淀**：
- 参考 finance-ledger 的 parser/config/recalc 模式

---

## 项目历史

### 2025-03-18 项目创建与优化
- **决策**: 创建日程管理系统
- **参考**: todo-manager + reminder Skill
- **核心设计**: 区分定时任务和普通待办

### 关键设计决策

#### 1. 任务分类（重要）
| 类型 | 说明 | 格式 |
|-----|------|------|
| **定时任务** | 需要提醒，有具体时间 | `YYYY-MM-DD HH:MM` |
| **普通待办** | 当天完成即可 | `YYYY-MM-DD` |

**原因**: 用户反馈时间标签混乱，明确区分后更清晰

#### 2. 数据格式
```markdown
- 2026-03-18 18:00 | [待办] | [P1高] | 吃饭 | #生活 | 提醒:准时
- 2026-03-18 | [待办] | [P2中] | 看电影 | #娱乐
```

#### 3. 继承性保障
- 符合 PATTERN-005 标准
- README.md 包含 GitHub 地址和恢复方法
- SYSTEM.md 包含完整 SOP 和示例

---

*用于记录项目迭代过程中的决策和教训*
