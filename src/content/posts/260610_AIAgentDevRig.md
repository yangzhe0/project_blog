---
title: '个人 AI Agent 研发环境搭建：Ubuntu 工作站与 RTX 5090 双机工作流'
published: 2026-06-10
description: '构建个人/实验室专属的 AI Agent 研发环境：本地 Ubuntu 24.04 开发机 + 远端 Threadripper & RTX 5090 算力机，打通 MCP、Obsidian、Ollama 与大模型工程链路。'
image: './image/260610_02.svg'
tags: [Ubuntu, GPU, Ollama, AI Agent, Work]
category: Work
draft: false
---

> 对于大模型与 AI Agent 开发者而言，在单台机器上既跑重型推理又搞日常开发，常常会遇到显存抢占、风扇轰鸣与系统卡顿等痛点。本文分享一套**“本地轻量开发工作站 + 远端专用 GPU 算力机”**的双机协作环境搭建方案，覆盖系统参数配置、Ollama 局域网服务化、MCP 工具层挂载与全链路联调。

---

## 一、双机拓扑架构与分工

```text
┌────────────────────────────────────────────────────────┐
│  本地工作站 (Ubuntu 24.04)                              │
│  - 承担角色: 日常编码、文档编写、Agent 流程编排、MCP 客户端 │
│  - 核心组件: VS Code / Codex / Obsidian / OpenClaw     │
└───────────────────────────┬────────────────────────────┘
                            │ (局域网 10GbE / 内网专线)
                            │ HTTP API (11434 / v1)
┌───────────────────────────▼────────────────────────────┐
│  远端算力机 (Dell Precision 7875 V2, Ubuntu 22.04)      │
│  - 硬件: AMD Threadripper PRO 9955WX (16C/32T), 128G   │
│  - GPU: NVIDIA RTX 5090 32GB                          │
│  - 服务: Ollama (OpenAI-compatible REST API)           │
│  - 承载模型: qwen3:30b (推理), nomic-embed-text (向量)  │
└────────────────────────────────────────────────────────┘
```

**核心优势**：
1. **静音与低功耗**：桌面日常开发机安静平稳，避免高负载推理导致桌面 UI 卡顿。
2. **算力即服务**：远端 GPU 服务器统一暴露标准的 OpenAI 兼容接口，课题组或个人多设备（笔记本、台式机、手机）均可共享调用。

---

## 二、远端 GPU 算力机配置

### 1. 硬件规格与驱动环境
- **CPU**：AMD Ryzen Threadripper PRO 9955WX
- **内存**：128GB DDR5 ECC
- **显卡**：NVIDIA RTX 5090 32GB (Driver 580+, CUDA 13.0+)
- **存储**：1TB NVMe 系统盘 + 4TB 企业级数据盘挂载于 `/data`

### 2. Ollama 服务化与局域网监听
在远端机配置 Systemd 环境变量，使其监听全局局域网网卡：

编辑 `/etc/systemd/system/ollama.service.d/override.conf`：

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_ORIGINS=*"
Environment="OLLAMA_KEEP_ALIVE=24h"
Environment="OLLAMA_NUM_PARALLEL=4"
```

重载并启动：
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### 3. 模型部署矩阵
```bash
# 1. 部署主力 30B 推理模型 (Q4_K_M 量化，显存占用约 24.9GB / 32GB)
ollama run qwen3:30b

# 2. 部署轻量兜底模型 (7B 级别，极速响应)
ollama run qwen2.5:7b-instruct

# 3. 部署高维文本向量嵌入模型
ollama run nomic-embed-text
```

---

## 三、本地开发机环境与工具链

### 1. 本机环境清单
- **操作系统**：Ubuntu 24.04 LTS (Kernel 6.17+)
- **开发工具**：Python 3.12、Node.js v24+、Docker 29+、ripgrep、tmux、fzf
- **AI 辅助工具**：Codex CLI、Claude Code、OpenClaw

### 2. 统一 OpenAI 兼容环境变量
在本地 `~/.bashrc` 或项目 `.env` 中声明：

```bash
export OPENAI_BASE_URL="http://192.168.180.234:11434/v1"
export OPENAI_API_KEY="ollama"  # Ollama 本地接口无需真实 Key，填占位符即可
export DEFAULT_CHAT_MODEL="qwen3:30b"
export DEFAULT_EMBEDDING_MODEL="nomic-embed-text"
```

---

## 四、打通 MCP 与知识库生态

通过 **Model Context Protocol (MCP)**，本地 Agent 可以无缝调用本机工具与 Obsidian 知识库：

1. **Obsidian Local REST API**：开启本地 API 插件，暴露端口与 Token。
2. **MCP Server 配置文件**：在开发机全局配置中挂载 `filesystem`、`git`、`obsidian` 以及 `fetch` 等基础 Servers。
3. **闭环体验**：当你在本地终端要求 Agent 总结某篇论文或审查代码时，Agent 自动通过 MCP 读取本地文件，调用远端 RTX 5090 上的 `qwen3:30b` 思考，并将产出结果直接写回 Obsidian Vault。

---

## 五、联调验证与性能体检

在本地开发机执行快速烟测脚本：

```bash
# 1. 验证模型列表连通性
curl -s http://192.168.180.234:11434/v1/models | jq .

# 2. 测试流式文本补全
curl -s http://192.168.180.234:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:30b",
    "messages": [{"role": "user", "content": "你好，请用一句话介绍你自己"}],
    "temperature": 0.3
  }' | jq .choices[0].message.content

# 3. 测试 768 维向量生成
curl -s http://192.168.180.234:11434/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "input": "AI Agent 开发环境测试"
  }' | jq '.data[0].embedding | length'
```

---

## 六、总结

这套双机方案兼顾了**开发的轻便性**与**大模型推理的高性能**。通过将重度算力剥离到远端服务器，本地保持整洁的开发与调试环境，配合 MCP 与 Ollama 标准化协议，为后续的 Agent 项目开发、学术情报监控与知识沉淀提供了坚固的基础底座。

