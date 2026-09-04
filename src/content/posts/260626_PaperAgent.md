---
title: 'PaperAgent：面向课题组论文库的本地 RAG 智能体'
published: 2026-06-26
description: '面向科研论文库的本地知识库智能体实战：基于 Streamlit + MinerU + Ollama + BGE-M3 + FAISS，实现高精度检索、确定性路由与跨文献深度对比。'
image: './image/260626_01.svg'
tags: [AI Agent, RAG, Streamlit, Research, Work]
category: Work
draft: false
---

> 在科研场景中，通用的 ChatGPT 往往无法直接处理课题组内部专属的 PDF 论文库，且容易出现胡编乱造、无法精确溯源等问题。`PaperAgent` 是一个完全**本地化部署的科研论文知识库 RAG 智能体**，旨在将复杂的学术论文解析为可结构化检索、支持跨篇比对、且每一条结论皆可严密追溯到原文切片的科研助手。

---

## 一、核心定位与技术栈

### 1. 核心解决的痛点
- **拒绝黑盒问答**：每个回答必须严格附带来源 PDF 文件名与原文引用切片。
- **结构化与 RAG 融合**：作者论文列表、特定天体数据源查询走确定性索引，开放式学术探讨走向量语义检索。
- **纯私有化运行**：数据不离开本地服务器，支持离线与局域网部署。

### 2. 技术栈选型

```text
前端界面: Streamlit (单页流式对话 Web UI)
文档解析: MinerU (高保真 PDF 转 Markdown) + pypdf
文本嵌入: BGE-M3 (本地多语言高精度 Embedding 模型)
向量存储: FAISS (本地高性能向量索引)
大模型推理: Ollama (本地部署 Qwen2.5 7B / Qwen3 30B)
调度编排: LangChain Community + 自研确定性路由引擎
```

### 3. 双档模型策略
- **Fast 模式 (`qwen2.5:7b-instruct`)**：用于日常高频名词解释、单篇快速问答与索引查找，响应极快。
- **Deep 模式 (`qwen3:30b`)**：用于长篇文献综合研读、多论文研究方法交叉对比与深度总结。

---

## 二、架构设计与混合检索链路

```text
[ 原始科研 PDF 论文库 ]
         │
         ▼ (MinerU 深度解析)
[ 结构化 Markdown 文本 ]
         │
         ▼ (切片: chunk_size=1100, overlap=180)
[ BGE-M3 向量化 ] ───► [ FAISS 本地向量库 + 结构化元数据索引 ]
                                  │
[ 用户学术提问 ]                   │
         │                        │
         ▼                        │
[ 查询路由器 (Query Router) ] ──────┤
   ├─ 1. 作者/关键词结构化查询 ────► 命中结构化索引直接返回
   ├─ 2. 跨对象数据源比对 ────────► 分解 Query 并行检索
   └─ 3. 开放式研究问答 ──────────► FAISS 语义相似度召回 (k=8)
                                  │
                                  ▼
[ 注入上下文 Prompt 模板 + Ollama 生成 ]
                                  │
                                  ▼
[ 流式输出回答 + 精准原文溯源片段 ]
```

---

## 三、特色：确定性路由（Query Router）

传统的 RAG 方案容易将所有问题一股脑丢进向量库，导致结构化事实（如“张教授一共有哪几篇关于海王星卫星的论文”）召回率低下甚至答非所问。

PaperAgent 采用了**层级路由机制**：
1. **作者 / 关键词清单**：直接查询由论文元数据预抽取的结构化倒排索引，秒级返回 100% 确定的论文列表。
2. **天体与数据源对比（如 Gaia DR2 vs DR3）**：将对比实体拆解为双向检索流，强制平衡两侧的召回片段，防止单一实体的文本覆盖另一侧。
3. **复杂理论与方法推导**：进入标准的 FAISS Top-K 语义检索，并经过 MMR（最大边际相关性）重排序后交由大模型生成解答。

---

## 四、部署与日常维护

### 1. 本地启动服务
```bash
# 1. 启动 Ollama 模型服务
ollama serve

# 2. 启动 Streamlit Web 端
streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port 8000 \
  --server.headless true
```

### 2. 论文库增量更新流水线
当课题组新增一批 PDF 论文时：
```bash
# 1. 将新 PDF 放入 data/papers/
# 2. 执行 MinerU 自动化解析
./scripts/parse_with_mineru.sh

# 3. 重新构建 FAISS 向量库与结构化索引
./scripts/rebuild_index.sh
```

---

## 五、总结

`PaperAgent` 的实践表明：在学术科研等高严肃性领域，**“确定性结构化索引 + 局部精准 RAG + 本地开源大模型”** 的组合，远比单纯依赖通用商业大模型更加可靠、透明且易于维护。

