---
title: 'Claude Code 命令速查：斜杠命令、全局参数与子命令'
published: 2026-09-03
description: '基于本机 Claude Code 2.1.259 实测整理的一份完整命令速查，覆盖 110 条斜杠命令、52 个全局参数与 18 个子命令。'
image: './image/260903_01.svg'
tags: [Claude Code, AI, Tutorial]
category: Notes
draft: false
---

> 记命令是件反人性的事。所以这一篇，我把 Claude Code 从「怎么启动」到「有哪些斜杠命令、参数、子命令」全部整理成一张可查的表。

Claude Code 的命令看起来多，其实只有三种形态：**斜杠命令**（进入 `claude` 之后敲 `/`）、**全局参数**（启动时附加 `--flag`）、**子命令**（`claude <子命令>`）。分清楚这三类，剩下的就是查表。

本文基于本机已安装的 **Claude Code 2.1.259**，命令与参数来自 `claude --help` 的实际输出，斜杠命令以官方文档为准。不同版本的命令可能略有差异（文末已标注本版本中被移除的几条），遇到疑问时运行 `claude --help` 或 `claude <命令> --help` 看本机说明，交互界面内输入 `/help` 看完整斜杠命令清单。

本文适合：

- 刚开始用 Claude Code、想快速摸清命令体系的人；
- 已经用了很久、但总想不起来某个斜杠命令拼法的人；
- 想在脚本 / CI 里做非交互调用（`-p`）的人。

## 目录

1. [三种形态怎么分](#一三种形态怎么分)
2. [斜杠命令](#二斜杠命令)
3. [全局参数](#三全局参数)
4. [子命令](#四子命令)
5. [安全提醒](#五安全提醒)

---

## 一、三种形态怎么分

| 形态 | 什么时候用 | 例子 |
|------|-----------|------|
| **斜杠命令** | 进入 `claude` 交互界面后，在输入框敲 `/` | `/help`、`/review`、`/compact` |
| **全局参数** | 启动 `claude` 时附加 `--flag` | `claude -p "..."`、`claude --model sonnet` |
| **子命令** | `claude` 后面跟一个动词 | `claude doctor`、`claude mcp add` |

一句话：**斜杠命令管「对话里做什么」，全局参数管「这次怎么跑」，子命令管「claude 这个工具本身的配置与诊断」。**

---

## 二、斜杠命令

### 会话与上下文

| 命令 | 作用 |
|------|------|
| `/help` | 显示帮助与可用命令。 |
| `/clear [name]` | 清空上下文开始新会话（别名 `/reset`、`/new`）。 |
| `/compact [instructions]` | 压缩对话，释放上下文空间。 |
| `/context [all]` | 用彩色网格可视化上下文占用，并给优化建议。 |
| `/export [filename]` | 把当前对话导出为纯文本。 |
| `/copy [N]` | 复制最近（或第 N 条）助手回复到剪贴板。 |
| `/resume [session]` | 按 ID / 名称恢复会话，或打开选择器。 |
| `/rewind` | 回退对话和/或代码到某个检查点。 |
| `/fork [prompt]` | 把当前对话复制成新的后台会话。 |
| `/branch [name]` | 在此处创建会话分支，尝试不同方向。 |
| `/background [prompt]` | 将会话转到后台运行（别名 `/bg`）。 |
| `/stop` | 停止当前后台会话。 |
| `/status` | 打开设置的状态页（版本 / 模型 / 账户 / 连接）。 |
| `/usage` | 查看用量与花费（别名 `/cost`、`/stats`）。 |
| `/goal [condition/clear]` | 设置跨轮次持续执行的目标。 |
| `/btw [question]` | 旁路提问，不写入对话历史。 |
| `/focus` | 切换焦点视图（只显示提示、工具摘要与最终回复）。 |
| `/recap` | 按需生成当前会话的一句话总结。 |
| `/rename [name]` | 重命名当前会话并显示在提示栏。 |
| `/diff` | 打开交互式 diff 查看器（未提交改动 + 每轮 diff）。 |
| `/tui [default/fullscreen]` | 切换 TUI 渲染模式。 |

### 模型、配置与权限

| 命令 | 作用 |
|------|------|
| `/model [model]` | 切换模型并设为新会话默认。 |
| `/effort [level/auto/status]` | 设置推理强度（low–xhigh、max、auto）。 |
| `/fast [on/off]` | 切换快速模式。 |
| `/config [key=value ...]` | 打开设置界面或直接改配置（别名 `/settings`）。 |
| `/theme` | 切换颜色主题（含跟随终端明暗的 auto）。 |
| `/color [color/default]` | 设置当前会话提示栏颜色。 |
| `/vim` | 已移除（v2.1.92），改用 `/config` → Editor。 |
| `/autocompact [auto/tokens]` | 设置自动压缩的上下文阈值。 |
| `/permissions` | 管理工具的 allow / ask / deny 规则（别名 `/allowed-tools`）。 |
| `/hooks` | 查看工具事件相关的 Hook 配置。 |
| `/keybindings` | 打开键盘快捷键配置文件。 |
| `/add-dir <path>` | 为当前会话添加工作目录。 |
| `/cd <path>` | 切换会话工作目录（保留对话）。 |
| `/memory` | 编辑 CLAUDE.md 并管理自动记忆。 |
| `/sandbox` | 切换沙箱模式（仅受支持平台）。 |
| `/statusline` | 配置状态栏。 |
| `/scroll-speed` | 交互式调整鼠标滚轮滚动速度。 |
| `/rate-limit-options` | 查看被限流时的续作选项。 |
| `/terminal-setup` | 安装 Shift+Enter 换行键绑定等终端配置。 |

### 审查、计划与任务

| 命令 | 作用 |
|------|------|
| `/init` | 为当前项目生成 CLAUDE.md 指令文件。 |
| `/plan [description]` | 进入计划模式，先规划再实施。 |
| `/review [...]` | 审查当前 diff（主命令 `/code-review`，可 `--fix` / `--comment`）。 |
| `/security-review` | 分析当前分支改动中的安全漏洞。 |
| `/simplify [target]` | 审查并清理改动的可复用 / 精简项。 |
| `/ultraplan <prompt>` | 已移除，改用 plan 模式。 |
| `/ultrareview [PR/branch]` | 云端沙箱多智能体深度审查。 |
| `/pr-comments [PR]` | 已移除（v2.1.91），直接让 Claude 查看 PR 评论。 |
| `/agents` | 提示创建 / 管理子代理（或直接编辑 `.claude/agents/`）。 |
| `/list-agents` | 列出子代理、队友与可通信会话（别名 `/peers`）。 |
| `/subtask <task>` | 派生子代理处理子任务并回报。 |
| `/tasks` | 查看管理后台任务与已完成的子代理。 |
| `/verify` | 构建 / 运行项目，确认改动达到预期。 |
| `/run` | 启动并驱动项目应用，查看改动真实效果。 |
| `/run-skill-generator` | 教 `/run`、`/verify` 如何构建 / 启动本项目。 |
| `/workflows` | 打开工作流进度视图（观看 / 暂停 / 恢复）。 |
| `/workflow-authoring` | 加载动态工作流编写参考。 |

### MCP、插件与集成

| 命令 | 作用 |
|------|------|
| `/mcp` | 管理 MCP 连接与 OAuth 认证。 |
| `/plugin [subcommand]` | 管理插件（list / install / enable / disable）。 |
| `/skills` | 列出可用 skills，可按名称 / 描述过滤。 |
| `/reload-plugins [--force]` | 不重启重新加载所有插件。 |
| `/reload-skills` | 重新扫描 skill 与命令目录。 |
| `/ide` | 管理 IDE 集成并显示状态。 |
| `/login` / `/logout` | 登录 / 登出 Anthropic 账号。 |
| `/bug [report]` | 反馈 Bug 或分享会话（别名 `/share`）。 |
| `/feedback [report]` | 发送产品反馈。 |
| `/import [codex/gemini]` | 从 Codex / Gemini 导入配置。 |
| `/install-github-app` | 为仓库安装 Claude GitHub App。 |
| `/install-slack-app` | 通过浏览器 OAuth 安装 Claude Slack App。 |
| `/web-setup` | 连接 GitHub 账号到 Claude Code on the web。 |
| `/setup-bedrock` | 配置 Amazon Bedrock。 |
| `/setup-vertex` | 配置 Google Vertex AI。 |

### 云、远程、语音与账户

| 命令 | 作用 |
|------|------|
| `/remote-control` | 启用 / 管理远程控制。 |
| `/remote-env` | 选择云端 agent 的默认环境。 |
| `/teleport` | 把 web 会话拉进当前终端。 |
| `/desktop` | 转到 Claude Code 桌面应用继续（别名 `/app`）。 |
| `/mobile` | 显示移动端下载二维码（别名 `/ios`、`/android`）。 |
| `/chrome` | 配置 Claude in Chrome 集成。 |
| `/voice [hold/tap/off]` | 切换语音输入。 |
| `/schedule [description]` | 创建 / 管理云端例程（routines）。 |
| `/upgrade` | 打开升级页面切换更高套餐。 |
| `/release-notes` | 在版本选择器中查看更新日志。 |
| `/usage-credits` | 配置用量额度或向管理员申请。 |
| `/team-onboarding` | 根据使用历史生成团队上手指南。 |
| `/privacy-settings` | 查看 / 更新隐私设置（Pro / Max）。 |
| `/insights` | 生成近期会话使用分析 HTML 报告。 |
| `/advisor [model/off]` | 启停顾问工具（关键时刻咨询第二模型）。 |
| `/artifacts` | 列出并附加拥有的 / 共享的 artifacts。 |
| `/auto-mode-setup` | 生成 autoMode.environment 配置。 |
| `/autofix-pr [prompt]` | 云端会话盯 PR，修 CI 失败与评论。 |
| `/passes` | 分享一周免费试用（符合条件才显示）。 |
| `/powerup` | 通过交互式教学了解功能。 |
| `/radio` | 浏览器打开 Claude FM 电台。 |
| `/stickers` | 订购 Claude Code 贴纸。 |
| `/heapdump` | 写 JS 堆快照（隐藏命令，用于排查内存）。 |

### 内置技能（bundled skills）

| 命令 | 作用 |
|------|------|
| `/code-review [level]` | 审查 diff / PR / 分支（`/review` 即其别名）。 |
| `/loop [interval] [prompt]` | 定时重复运行某条提示（别名 `/proactive`）。 |
| `/dataviz [request]` | 图表 / 可视化的设计规范指导。 |
| `/debug [description]` | 启用调试日志并读取会话日志排障。 |
| `/deep-research <question>` | 联网搜索 + 交叉验证 + 生成带引用报告。 |
| `/design [brief]` | 生成 UI 草图 / 流程图 / 落地页。 |
| `/design-login` | 授权设计系统访问。 |
| `/design-sync [hint]` | 把 React 设计系统同步上传到 Claude Design。 |
| `/claude-api [...]` | 加载 Claude API / Managed Agents 参考（迁移、升级、审计等）。 |
| `/batch <instruction>` | 研究、分解并并行执行大规模改动。 |
| `/fewer-permission-prompts` | 扫描会话并生成权限白名单，减少弹窗。 |

---

## 三、全局参数

### 常用参数

| 参数 | 含义 | 示例 |
|------|------|------|
| `-p` / `--print` | 非交互打印输出后退出，适合管道与 CI。 | `claude -p "..."` |
| `-c` / `--continue` | 继续当前目录最近一次会话。 | `claude -c` |
| `-r` / `--resume [id]` | 恢复指定会话 ID，或打开会话选择器。 | `claude -r` |
| `--model` | 指定模型，可用别名 `fable` / `opus` / `sonnet` 或全名。 | `claude --model sonnet` |
| `--fallback-model` | 主模型过载时自动回退（仅 `--print`）。 | `--fallback-model haiku` |
| `--effort` | 推理强度：low / medium / high / xhigh / max。 | `claude --effort high` |
| `--add-dir` | 额外授予某个目录访问权限，可重复使用。 | `claude --add-dir ../shared` |
| `--permission-mode` | 权限模式：acceptEdits / plan / bypassPermissions / manual / dontAsk / auto。 | `claude --permission-mode plan` |
| `--allowedTools` / `--disallowedTools` | 允许 / 禁止指定工具（逗号或空格分隔）。 | `--allowedTools "Bash(git *) Edit"` |
| `--tools` | 指定内置工具集；`""` 禁用全部，`default` 全部启用。 | `--tools "Bash,Edit,Read"` |
| `--output-format` | 输出格式：text / json / stream-json（仅 `--print`）。 | `--output-format json` |
| `--input-format` | 输入格式：text / stream-json（仅 `--print`）。 | `--input-format stream-json` |
| `--max-turns` / `--max-budget-usd` | 限制最大轮次 / API 花费上限（仅 `--print`）。 | `--max-turns 5 --max-budget-usd 1` |
| `--append-system-prompt` | 在默认系统提示后追加内容。 | `--append-system-prompt "你是安全专家"` |
| `--system-prompt` | 自定义本次会话的系统提示。 | `--system-prompt "你是 Rust 专家"` |
| `--session-id` | 用固定 UUID 作为会话 ID。 | `--session-id <UUID>` |
| `--fork-session` / `--from-pr` | 恢复时新建会话 ID / 按 PR 恢复关联会话。 | `--continue --fork-session` |
| `--mcp-config` / `--strict-mcp-config` | 从 JSON 文件加载 MCP；strict 则忽略其他 MCP 配置。 | `--mcp-config ./mcp.json` |
| `--settings` | 加载额外设置文件或 JSON 字符串。 | `--settings ./settings.json` |
| `--restricted` / `--safe-mode` | 受限模式（禁用运行命令的工具）/ 安全模式（禁用全部自定义）。 | `claude --safe-mode` |
| `-w` / `--worktree` | 为本会话创建新的 git worktree。 | `claude -w` |
| `--bg` / `--background` | 后台启动会话并立即返回 ID。 | `claude --bg` |
| `--verbose` / `-d` / `--debug` | 详细输出 / 调试模式（可带类别过滤）。 | `claude -d` |
| `--json-schema` | 结构化输出校验（JSON Schema）。 | `--json-schema '{"type":"object",...}'` |
| `-n` / `--name` | 设置会话显示名。 | `claude -n "重构"` |
| `--ide` | 启动时自动连接唯一可用 IDE。 | `claude --ide` |

### 进阶参数

| 参数 | 含义 |
|------|------|
| `--agent` / `--agents` | 指定会话 agent / 用 JSON 定义自定义 agents。 |
| `--allow-dangerously-skip-permissions` | 把「跳过权限」作为可选项（不默认启用）。 |
| `--autocompact <auto/tokens>` | 设置自动压缩的上下文阈值。 |
| `--bare` | 极简模式：跳过 hooks、LSP、插件、CLAUDE.md 自动发现等。 |
| `--chrome` / `--no-chrome` | 启用 / 禁用 Claude in Chrome 集成。 |
| `--cloud` | 创建云端会话，或按 ID / URL 接入已有会话。 |
| `--debug-file <path>` | 调试日志写入指定文件（隐式开启调试）。 |
| `--disable-slash-commands` | 禁用全部 skills。 |
| `--environment <id>` | 在指定自托管环境创建云端会话。 |
| `--file <specs>` | 启动时下载文件资源（file_id:relative_path）。 |
| `--no-session-persistence` | 禁用会话持久化，不落盘、不可恢复（仅 `--print`）。 |
| `--permission-prompts <host/none>` | 谁回答权限提示：host 或 none（自动拒绝）。 |
| `--plugin-dir` / `--plugin-url` | 临时加载插件（目录 / zip / URL，可重复）。 |
| `--prompt-suggestions` | 启用提示建议（print/SDK 模式）。 |
| `--remote-control` | 以远程控制方式启动交互会话。 |
| `--setting-sources` | 指定加载的设置来源（user/project/local）。 |
| `--teleport` | 恢复 teleport 会话。 |
| `--tmux` | 为 worktree 创建 tmux 会话（需 `--worktree`）。 |
| `--ax-screen-reader` | 屏幕阅读器友好输出（无装饰边框/动画）。 |
| `--betas` / `--brief` | Beta 头（仅 API key）/ 启用 agent↔user 通信工具。 |
| `--include-partial-messages` | 流式输出中附带部分消息块（stream-json）。 |
| `--include-hook-events` | 输出流中包含全部 hook 生命周期事件（stream-json）。 |
| `--replay-user-messages` | 把 stdin 用户消息回显到 stdout（stream-json）。 |
| `--forward-subagent-text` | 转发子代理文本/思考块（`--print` + stream-json）。 |
| `--system-prompt-snapshot <on/off>` | 是否记录并复用系统提示（默认内置提示为 on）。 |
| `--exclude-dynamic-system-prompt-sections` | 把按机器变化的部分移出系统提示，提升 prompt 缓存复用。 |

### 常用用法示例

非交互执行，适合脚本 / CI：

```bash
claude -p "运行测试并修复失败"
```

JSON 输出，便于解析：

```bash
claude -p "列出 TODO" --output-format json
```

流式 JSON 输出（供 Agent SDK 使用）：

```bash
claude -p "..." --output-format stream-json
```

流式 JSON 输入（从 stdin 持续读消息）：

```bash
claude -p --input-format stream-json --output-format stream-json
```

限制工具集与轮次预算：

```bash
claude -p "..." --allowedTools "Bash(git *) Edit" --max-turns 5 --max-budget-usd 1
```

---

## 四、子命令

### 启动

| 命令 | 作用 |
|------|------|
| `claude` | 启动交互界面，随后直接描述任务。 |
| `claude "检查项目并运行测试"` | 带初始任务启动。 |
| `claude --help` | 查看当前版本支持的完整命令和参数。 |
| `claude --version` | 查看版本号。 |

### 会话与后台

| 命令 | 作用 |
|------|------|
| `claude --bg "跑全量测试"` | 会话转到后台运行，立即返回会话 ID。 |
| `claude agents` | 列出后台运行中的会话及其 ID。 |
| `claude attach <ID>` | 把某个后台会话拉回当前终端。 |
| `claude logs <ID>` | 打印后台会话最近的终端输出。 |
| `claude stop <ID>` / `claude rm <ID>` | 停止会话（保留对话）/ 删除已退出的会话。 |
| `claude respawn <ID>` | 以当前版本重启后台会话（`--all` 重启全部）。 |

### 代码审查

| 命令 | 作用 |
|------|------|
| `claude ultrareview` | 对当前分支或 PR 跑云托管多智能体审查。 |
| `claude ultrareview 123` | 审查某个 PR 编号或基准分支。 |

### 认证

| 命令 | 作用 |
|------|------|
| `claude auth login` | 使用 Anthropic 账号登录。 |
| `claude auth status` | 查看登录状态，适合脚本判断凭据是否存在。 |
| `claude auth logout` | 清除当前登录凭据。 |
| `claude setup-token` | 为订阅用户设置长期认证令牌。 |

### MCP 服务器管理

| 命令 | 作用 |
|------|------|
| `claude mcp add my-server -- npx my-mcp-server` | 添加 stdio 服务器，`--` 分隔命令与参数。 |
| `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` | 添加 HTTP 服务器，可带请求头。 |
| `claude mcp add my-server -e API_KEY=xxx -- npx my-mcp-server` | 添加时通过 `-e KEY=value` 注入环境变量。 |
| `claude mcp list` / `claude mcp get <name>` | 列出已配置服务器 / 查看单个详情。 |
| `claude mcp remove <name>` | 移除某个 MCP 服务器。 |
| `claude mcp serve` | 把 Claude Code 自身作为 MCP 服务器暴露。 |

### 插件管理

| 命令 | 作用 |
|------|------|
| `claude plugin install my-plugin` | 从市场安装，可指定 `插件@市场`。 |
| `claude plugin list` | 查看已安装插件列表。 |
| `claude plugin uninstall my-plugin` | 卸载已安装插件。 |
| `claude plugin marketplace add <repo>` | 添加插件市场仓库。 |

### 诊断、迁移与更新

| 命令 | 作用 |
|------|------|
| `claude doctor` | 检查认证、配置、Git、终端等常见问题。 |
| `claude update` | 检查并安装可用更新。 |
| `claude install stable` | 安装原生构建，可指定 stable / latest / 具体版本。 |
| `claude import codex` | 从 Codex / Gemini 导入配置（`--dry-run` 预览）。 |
| `claude project purge` | 删除某项目的全部 Claude 状态（会话、任务等）。 |
| `claude auto-mode` | 查看或重置自动模式分类器配置。 |
| `claude gateway` | 运行企业认证 / 遥测网关。 |

---

## 五、安全提醒

> `--dangerously-skip-permissions` 会跳过所有权限检查，等同让 Claude 自动执行全部命令，**仅建议在无外网的沙箱中使用**。

日常建议保留默认审批，或按需收窄：

- `--permission-mode plan`：只规划、不动手；
- `--permission-mode acceptEdits`：仅自动接受文件编辑；
- `--restricted`：受限模式，禁用运行命令的工具；
- `--safe-mode`：安全模式，禁用全部自定义配置。

从保守到激进，优先级由低到高排好，多数日常场景用默认审批就够。

---

> **版本说明：**`/vim`（v2.1.92 起移除）、`/pr-comments`（v2.1.91 起移除）、`/ultraplan`（已移除）在本版本中不再可用。命令以本机 `claude --help` 与官方文档为准，升级后如有出入，以 `claude --help` 为准。
