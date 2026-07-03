# OpenXterm 规格说明书

## 1. 项目概述

OpenXterm 是一个轻量级 SSH 客户端（Windows 桌面应用），核心目标是**保存连接配置和密码**，让用户一键连接，无需重复输入密码。

## 2. 核心功能

### 2.1 连接管理
- 保存 SSH 连接（主机、端口、用户名、密码、跳板机配置等）
- 支持 SSH 端口转发参数：-L、-R、-D、-J（跳板机）
- 支持从自定义命令字符串解析并保存连接参数

### 2.2 密码管理
- 密码本地加密存储（使用 Fernet 加密）
- 密码可见切换（小眼睛按钮，明文/密文切换显示）
- 支持手动填入密码，也支持从命令字符串中解析并自动保存密码

### 2.3 连接执行
- 启动系统 OpenSSH 客户端（ssh.exe）执行连接
- 管道输入密码自动应答

### 2.4 UI 界面
- 连接列表，显示：名称、主机、端口、用户名
- 新建连接对话框/表单
- 小眼睛密码显示切换
- 一键连接按钮
- 编辑/删除连接

## 3. 非功能需求
- 最小实现：本地 SQLite 存储 + Tkinter 简单界面
- Windows 10+ 兼容
- 打包为单个 exe 安装包
- 离线运行，无网络依赖

## 4. 技术栈
- Python 3.10+
- Tkinter（内置 GUI 库）
- cryptography（Fernet 加密密码存储）
- PyInstaller（打包 exe）
- sqlite3（内置数据库）

## 5. 数据模型

```
Connection:
  id            INTEGER PRIMARY KEY AUTOINCREMENT
  name          TEXT              -- 连接名称(别名)
  host          TEXT NOT NULL     -- 主机名/IP
  port          INTEGER DEFAULT 22
  username      TEXT NOT NULL
  password      TEXT              -- 加密后的密码
  jump_host     TEXT              -- 跳板机主机
  jump_port     INTEGER DEFAULT 22
  jump_user     TEXT              -- 跳板机用户名
  jump_password TEXT              -- 跳板机密码(加密)
  extra_args    TEXT              -- 额外命令行参数
  created_at    TIMESTAMP
  updated_at    TIMESTAMP
```

