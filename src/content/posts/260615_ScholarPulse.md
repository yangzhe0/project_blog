---
title: 'ScholarPulse：本地优先的学术情报监测与自动化流水线'
published: 2026-06-15
description: '一条面向个人知识库的本地优先学术情报流水线：从 arXiv 定向检索、去重、Ollama 结构化中文研判，到 Obsidian 原子落盘与 Telegram 自动投递。'
image: './image/260615_01.svg'
tags: [AI Agent, Academic, Workflow, Ollama, Work]
category: Work
draft: false
---

> 在信息爆炸时代，跟踪前沿论文（如 AI Agent、RAG、MCP）往往让人疲惫不堪。`ScholarPulse` 是一条面向个人知识库的**本地优先（Local-first）学术情报监测流水线**。它的核心定位不是让 AI 随意“泛泛写个摘要”，而是将检索、去重、结构化研判、原子落盘、总索引维护与多端消息投递拆解为一条**确定、可测试、可审计**的工程生产链路。

---

## 一、核心设计哲学与架构原则

### 1. 为什么拒绝纯 Agent “黑盒化”？
传统的直接让 Agent 抓取并总结的方式往往存在三个痛点：
- **不可控与幻觉**：Prompt 波动可能导致抓漏论文或随意编造实验结论；
- **难以审计**：论文版本更新（如 `v1` 到 `v2`）容易造成重复收录；
- **状态脆弱**：一旦网络或模型短暂抖动，整个定时任务容易全军覆没。

### 2. 四大架构原则
1. **确定性核心（Deterministic Core）**：
   - 检索、去重、模板渲染与本地落盘完全由 Python CLI 负责，状态码明确、行为可回溯。
2. **Agent 解耦（Decoupled Consumer）**：
   - 消息网关（OpenClaw）只作为下游消费者读取格式化好的 JSON，不参与上游内容生产与抓取。
3. **本地知识主权（Local-first Knowledge）**：
   - 日报和索引文件直接原子写入本地 Obsidian Vault，无需依赖外部云数据库或消息队列。
4. **配置驱动（Configuration Driven）**：
   - 增加新的研究方向（如具身智能、量子计算）只需增加几行 JSON 配置，无需重构任何脚本代码。

---

## 二、生产与投递工作流

```text
[ systemd user timer (每天 19:55) ]
       │
       ▼
[ Python CLI: scholarpulse generate ]
       ├─ 1. arXiv API 检索 (AI Agent / MCP / RAG 关键词)
       ├─ 2. 归一化去重 (过滤历史收录与跨版本重复)
       ├─ 3. Ollama 本地模型 (生成 4 段式结构化中文研判)
       ├─ 4. 原子写入 Obsidian Vault (生成日报 + 重建全局索引)
       └─ 5. 输出当天通知 JSON (message, title, metrics)
       │
       ▼
[ OpenClaw Telegram 投递 (每天 20:00) ]
       └─ 读取通知 JSON，一键推送至移动端
```

---

## 三、关键流水线实现细节

### 1. 归一化去重机制
arXiv 论文常有多个版本提交。ScholarPulse 在入库前会正则剔除版本后缀：
```text
2606.12345v1 ──┐
2606.12345v2 ──┴──> 归一化 ID: 2606.12345 (查重键)
```
CLI 自动比对历史索引库，确保同一篇论文不会因为版本迭代在日报中反复刷屏。

### 2. Ollama 结构化研判约束
每篇论文的摘要生成严格遵循结构化模板，拒绝空话套话：
- **一句话结论**：论文解决的核心矛盾是什么。
- **核心内容**：具体提出的技术架构或算法创新。
- **方法与实验**：评测基准（Benchmark）与关键指标提升。
- **价值判断**：对实际工程落地的参考意义与局限性。

若模型服务临时不可用，流水线会自动填入备用原文信息，保证定时任务安全完成，绝不伪造虚假摘要。

### 3. 日报与总索引维护
生成的日报以标准 Frontmatter 写入 Obsidian：

```yaml
---
title: ScholarPulse-2026-06-15
published: 2026-06-15
tags: [AI-Agent, Academic, Report]
category: 科研
---
```

同时，系统会自动更新该研究方向的 `index.md` 索引页，按时间倒序维护全部历史报告入口，形成个人专属的长期学术情报库。

---

## 四、常用操作命令

```bash
# 生成当天所有配置方向的学术情报
scholarpulse generate

# 补跑或重算指定历史日期
scholarpulse generate --date 2026-05-15

# 单独调试指定方向（如仅跑 Agent 方向）
scholarpulse generate --direction AgentPulse

# 强行覆盖重建（人工修复时使用）
scholarpulse generate --force
```

---

## 五、总结与展望

通过将大语言模型（LLM）定位为**“确定性流水线中的文本处理算子”**，而非全盘委托给不可控的自主 Agent，`ScholarPulse` 实现了高可靠、零维护的个人学术情报持续沉淀。未来这套架构可轻松扩展至 GitHub Trending 监控、行业技术资讯聚合等更多自动化场景。

