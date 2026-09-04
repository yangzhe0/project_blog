---
title: 'OpenClaw 从 0 到 1：个人 AI 助手部署与维护实战'
published: 2026-06-10
description: '基于 Ubuntu 24.04 工作站与局域网 GPU 服务器，从 0 到 1 部署 OpenClaw 个人 AI 助手：涵盖 Gateway 配置、Telegram 接入、Obsidian MCP 联动与长期记忆系统。'
image: './image/260610_01.svg'
tags: [AI Agent, OpenClaw, Ollama, Ubuntu, Work]
category: Work
draft: false
---

> 本文记录在工位 Ubuntu 24.04 开发机上从 0 到 1 部署 **OpenClaw** 个人 AI 助手的完整工程落地过程。目标是打造一个既能在本地终端、网页端直接交互，又能通过 Telegram 移动端随叫随到，并且深度打通 Obsidian 个人知识库与远端 GPU 大模型的全天候智能助手。

---

## 一、架构设计与核心目标

### 1. 核心目标
- **多端入口**：通过 OpenClaw Gateway 提供本机 Web Dashboard / REST 入口，并通过 Telegram Bot 提供移动端即时交互。
- **算力分离**：本地工位机轻量运行 Agent 编排；远端 GPU 服务器（RTX 5090）运行 Ollama，承载 `qwen3:30b` 大模型与 `nomic-embed-text` 嵌入模型。
- **知识库打通**：通过 MCP（Model Context Protocol）读写本地 Obsidian Vault，赋予 Agent 检索与整理知识库的能力。
- **持久化长期记忆**：基于向量检索实现跨会话的长期记忆沉淀与召回。

### 2. 拓扑架构

```text
[ 移动端 Telegram ] <---+
                       | (HTTPS Proxy)
[ 本地 Web Dashboard ] <-+--> [ OpenClaw Gateway (端口: 18789) ]
                                |
                                +--> [ 本地 Obsidian Vault (MCP Server) ]
                                +--> [ 长期记忆系统 (Memory Vector Store) ]
                                +--> [ 远端 Ollama GPU 服务器 (192.168.x.x:11434) ]
                                       ├── qwen3:30b (主推理模型, 64k 上下文)
                                       └── nomic-embed-text (向量嵌入)
```

---

## 二、Gateway 服务化与代理配置

### 1. Systemd User Service 配置
为了保证网关在开机后自动拉起且不依赖 root 权限，采用 Systemd 用户级服务管理：

创建 `~/.config/systemd/user/openclaw-gateway.service`：

```ini
[Unit]
Description=OpenClaw Gateway Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/node /home/y/.npm-global/lib/node_modules/openclaw/dist/index.js gateway --port 18789
Restart=always
RestartSec=5
Environment=OPENCLAW_GATEWAY_PORT=18789

[Install]
WantedBy=default.target
```

### 2. 局部代理注入策略
由于 Telegram Bot 需要访问境外 API，而远端 Ollama 及局域网资源无需代理，推荐使用 Systemd Drop-in 配置局部代理，避免全局环境变量污染：

创建 `~/.config/systemd/user/openclaw-gateway.service.d/proxy.conf`：

```ini
[Service]
Environment="HTTPS_PROXY=http://127.0.0.1:7897"
Environment="HTTP_PROXY=http://127.0.0.1:7897"
Environment="ALL_PROXY=http://127.0.0.1:7897"
Environment="NO_PROXY=localhost,127.0.0.1,::1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,.local"
```

加载并启动：
```bash
systemctl --user daemon-reload
systemctl --user enable --now openclaw-gateway
```

---

## 三、模型接入与性能调优

在 `~/.openclaw/openclaw.json` 中配置远端 Ollama Provider：

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://192.168.180.234:11434",
        "api": "ollama",
        "timeoutSeconds": 300,
        "models": [
          {
            "id": "qwen3:30b",
            "reasoning": true,
            "contextWindow": 65536,
            "maxTokens": 8192,
            "params": {
              "num_ctx": 65536,
              "keep_alive": "15m",
              "temperature": 0.3
            }
          },
          {
            "id": "qwen2.5:7b-instruct",
            "reasoning": false,
            "contextWindow": 32768,
            "maxTokens": 8192,
            "params": {
              "num_ctx": 32768,
              "keep_alive": "15m"
            }
          }
        ]
      }
    }
  }
}
```

**调优要点**：
- **上下文扩容**：将 `num_ctx` 设为 `65536`，在 RTX 5090 32GB 显存上 `qwen3:30b (Q4_K_M)` 显存占用约为 24.9GB，留有足够裕量防止 OOM。
- **Keep Alive**：设置 `keep_alive: "15m"`，避免模型在频繁调用间反复重新加载到显存。

---

## 四、知识库与工具层（MCP & Telegram）

### 1. Telegram 移动端通道
运行 `openclaw channels add telegram`，根据向导填入 BotFather 申请的 Token。配置完成后，可以在手机随时随地给 Bot 发送语音、文字指令，由 Agent 在后台执行并回传处理结果。

### 2. Obsidian MCP Server 联动
将 Obsidian 笔记库作为外部知识源挂载给 Agent：
1. 在 Obsidian 中启用 Local REST API 插件；
2. 在 OpenClaw 中配置 `obsidian` MCP Server 规则；
3. Agent 获得 `search_notes`、`read_note`、`append_note`、`patch_note` 等原子工具能力，能够自主查阅过往笔记或将研究结论直接沉淀回 Vault。

### 3. 长期记忆机制
配置 Embedding 模型为 `nomic-embed-text`，OpenClaw 会在后台自动对关键事实、用户偏好和历史决策进行向量化落盘。当用户提及历史话题时，Agent 会通过语义检索自动召回相关背景，实现真正的连贯记忆。

---

## 五、日常维护与常用命令

```bash
# 查看整体运行状态与各通道健康度
openclaw status --deep

# 查看已注册的 MCP 工具与状态
openclaw mcp list

# 实时查看网关日志
journalctl --user -u openclaw-gateway -f -n 50

# 手动触发安全审计
openclaw security audit
```

---

## 六、总结

通过本套方案，我们实现了：
1. **低成本高效算力**：开发机轻巧无噪音，大模型算力集中在局域网高性能机器上；
2. **多模态全场景触达**：既有本地 Web Dashboard 供深度编码与调试，又有 Telegram 随时随地处理碎片化灵感；
3. **知识闭环**：通过 MCP 真正让 Agent 与个人知识库融为一体。

