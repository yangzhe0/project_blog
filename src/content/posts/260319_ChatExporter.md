---
title: 'Trae Chat Exporter：把 Trae 对话导出为 HTML/MD/JSON'
published: 2026-03-19
description: '基于 Trae 远程调试页面的本地导出工具，支持将聊天记录导出为 HTML、Markdown 和 JSON 格式，适合保存长对话和整理聊天记录。'
image: './image/260319_01.png'
tags: [Python, Tool]
category: Work
draft: false
---

前几天需要把 Trae 里的一些对话导出来，翻了半天没找到现成的工具，干脆自己写了一个。

![developer terminal code screen](https://images.unsplash.com/photo-1515879218367-8466d910aaa4?ixid=M3w4OTk5MTN8MHwxfHNlYXJjaHwxfHxkZXZlbG9wZXIlMjB0ZXJtaW5hbCUyMGNvZGUlMjBzY3JlZW58ZW58MHx8fHwxNzg4NTEyNzIzfDA&ixlib=rb-4.1.0&w=600&h=400&fit=crop&q=80)
*Photo by [Chris Ried](https://unsplash.com/@cdr6934) on [Unsplash](https://unsplash.com)*

## 这玩意能干嘛

把 Trae 当前打开的对话导出成三种格式：

- **HTML**：本地阅读体验最好，接近原聊天界面
- **Markdown**：只保留核心正文，方便整理和编辑
- **JSON**：保留原始消息数据，适合二次处理

## 怎么用

环境要求：Windows 桌面版 Trae + Python 3.10+

```powershell
# 安装依赖
python -m pip install -r .\requirements.txt

# 运行
powershell -ExecutionPolicy Bypass -File .\launch_trae_export.ps1
```

运行后脚本会自动关闭旧 Trae，以调试模式重启。然后你在 Trae 里登录、打开目标会话，等终端提示扫描完成，去 `exports` 目录拿结果就行。

## 几个细节

- 长对话会自动预热 + 多轮滚动扫描，尽量导完整
- 文件按会话名自动命名
- HTML 是结构保真，不是像素级克隆

## 项目地址

[https://github.com/yangzhe0/Trae_Chat_Exporter](https://github.com/yangzhe0/Trae_Chat_Exporter)

有问题提 Issue，觉得有用给个 Star。



