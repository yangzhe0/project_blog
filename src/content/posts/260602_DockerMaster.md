---
title: 'Docker 小白到大师'
published: 2026-06-02
description: '从第一条命令到容器化真实项目的 Docker 入门路线。'
image: './image/260602_01.svg'
tags: [Docker, Tutorial]
category: Notes
draft: false
---

> 这不是一篇概念堆叠的 Docker 笔记，而是一条可以照着做的学习路线：从第一条命令，到容器化一个真实项目。

---

## 为什么要学 Docker

Docker 解决的不是炫技问题，而是运行和交付问题。

一个项目在你电脑上能跑，不代表在服务器、同事电脑、测试环境里也能跑。Docker 的价值，就是把运行环境、依赖、启动方式尽量封装成一个清楚的交付物。

它带来的核心收益可以概括成三点：

- 环境一致
- 交付物清楚
- 回滚更简单

后面的每一条命令，其实都围绕这三个目标展开。

---

## 先确认 Docker 能不能跑

安装完成以后，不要急着上项目，先用三条命令验证环境。

```powershell
docker version
docker info
docker run hello-world
```

`docker version` 用来看客户端和服务端版本，`docker info` 用来看 Docker 引擎状态，`docker run hello-world` 用来验证镜像能拉取、容器能启动。

看到 `Hello from Docker`，就说明基本环境已经通了。

---

## 跑第一个真正的容器

接下来启动一个 nginx 容器：

```powershell
docker run --name web -d -p 8080:80 nginx:alpine
```

这条命令会把宿主机的 `8080` 端口映射到容器里的 `80` 端口。打开浏览器访问：

```text
http://localhost:8080
```

如果能看到 nginx 欢迎页，就说明你已经完成了第一个可访问服务。

把 `docker run` 拆开看，其实并不复杂：

- `--name web`：给容器起名
- `-d`：后台运行
- `-p 8080:80`：端口映射
- `nginx:alpine`：使用的镜像

以后大多数 `run` 命令，都是在这些部件上变化。

---

## 容器运行后怎么观察

容器启动以后，第一件事是看它到底有没有在跑。

```powershell
docker ps
docker ps -a
```

`docker ps` 查看正在运行的容器，`docker ps -a` 查看所有容器，包括已经退出的。

遇到问题时，先看日志：

```powershell
docker logs web
docker logs -f web
```

`docker logs -f` 可以持续跟随输出。启动失败、请求异常、服务报错，通常都能先从日志里看到线索。

如果要进入容器内部观察现场，可以用：

```powershell
docker exec -it web sh
```

进去以后可以检查文件、环境变量、网络连通性。排查完用 `exit` 退出。

---

## 镜像和容器是什么关系

镜像和容器的关系，可以理解成模板和实例。

镜像是只读模板，容器是镜像运行起来的实例。一个镜像可以启动多个容器，删除容器不等于删除镜像。

不用的容器可以先停止，再删除：

```powershell
docker stop web
docker rm web
```

临时容器确认不要了，也可以强制删除：

```powershell
docker rm -f web
```

注意：删除容器不会删除镜像，但容器可写层里的临时数据可能会丢。

---

## 用 Dockerfile 构建自己的镜像

Dockerfile 是把项目做成镜像的说明书。

一个典型 Dockerfile 会做几件事：

- 选择基础镜像
- 设置工作目录
- 安装依赖
- 复制源码
- 指定启动命令

写好 Dockerfile 后，可以构建镜像：

```powershell
docker build -t my-node-app:1.0 .
```

`-t` 后面是镜像名和标签，最后的 `.` 表示当前目录是构建上下文。

构建成功后查看镜像：

```powershell
docker images
```

自己的镜像构建好以后，就能像官方镜像一样运行：

```powershell
docker run --rm -p 3000:3000 my-node-app:1.0
```

浏览器能打开，就说明镜像可运行。

---

## `.dockerignore` 很重要

`.dockerignore` 决定哪些文件不要进入构建上下文。

常见应该排除的内容包括：

- `node_modules`
- `.git`
- `.env`
- 日志文件
- 测试覆盖率目录

它能让构建更快，也能避免把不该进镜像的敏感文件带进去。

---

## 端口、数据和网络

端口映射按“左边宿主机，右边容器”来记。

```powershell
-p 8080:80
```

意思是访问宿主机 `8080`，会转到容器里的 `80`。端口不通时，先看这个方向有没有写反。

数据库数据不要只放在容器可写层。更稳的方式是用 volume：

```powershell
docker volume create app-data
```

本地开发时，bind mount 也很常见。它可以把宿主机目录挂到容器里，方便用容器里的运行时处理本地代码。

容器之间通信时，不要总是绕宿主机端口。把服务放到同一个 Docker network 里，就可以用服务名访问。

例如 Redis 容器叫 `redis`，同一网络里的其他容器就可以直接用 `redis` 这个名字连接。

---

## 用 Compose 管理一组服务

真实项目通常不是一个容器，而是一组服务：Web、数据库、缓存、队列。

Compose 用一个 YAML 文件管理这组服务。本地开发时，一条命令就能拉起整套环境：

```powershell
docker compose up -d
```

常见组合是：

- `web`
- `db`
- `redis`

Compose 会自动创建网络，服务之间可以用 `web`、`db`、`redis` 这些名字互相访问。

查看日志：

```powershell
docker compose logs -f web
```

---

## 配置和密钥

配置应该在运行时注入，不要写死在镜像里。

同一个镜像可以跑在开发、测试和生产环境，只是环境变量不同。镜像负责能力，环境变量负责差异。

密钥尤其不要写进 Dockerfile，也不要 `COPY .env` 到镜像里。镜像层和构建历史都可能留下痕迹。

更稳的做法是：

- 平台 secret
- CI 密钥管理
- 运行期环境变量
- 挂载密钥文件

---

## 排障顺序

排障不要盲猜，先判断问题发生在哪个阶段。

| 问题 | 优先检查 |
| --- | --- |
| 构建失败 | Dockerfile、构建上下文、依赖安装 |
| 启动退出 | `docker logs` |
| 端口不通 | `docker ps`、端口映射 |
| 数据丢失 | volume / bind mount |
| 磁盘占满 | `docker system df` |

这套顺序能省掉很多无效尝试。

---

## 上线前检查

上线前至少检查这些点：

- 不要使用 `latest`
- 尽量非 root 运行
- 密钥不要进入镜像
- 数据使用 volume，并有备份
- 日志输出到标准输出
- 镜像版本可以回滚

Docker 不是只会启动容器就算学会。真正掌握，是能稳定构建、交付、运行、排障和回滚。

下一步就拿一个真实项目，按这套流程容器化一遍。
