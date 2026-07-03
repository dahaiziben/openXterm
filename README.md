# OpenXterm

轻量级 SSH 连接管理器 --- 保存连接配置和密码，一键连接，无需重复输入。

## 功能特性

- **保存 SSH 连接**: 主机、端口、用户名、密码、跳板机
- **小眼睛密码切换**: 点击按钮显示/隐藏密码明文
- **SSH 命令解析**: 粘贴 ssh 命令自动提取连接参数
- **端口转发**: 支持 -L, -R, -D, -J (跳板机)
- **一键连接**: 双击或点击按钮启动 SSH
- **密码加密存储**: 使用 Fernet 加密，安全存储

## 快速使用

### 直接运行 (无需打包)
`
python src/main.py
`

### 构建 exe 安装包
1. 双击 build.bat（自动安装 PyInstaller 并构建）
2. 生成 dist/OpenXterm.exe

### 快速安装
双击 install.bat 创建快捷方式

## 项目结构
`
src/main.py    -- GUI 主程序
src/crypto.py  -- 密码加解密
src/db.py      -- SQLite 数据库
src/parser.py  -- SSH 命令解析
build.bat      -- exe 构建脚本
setup.iss      -- Inno Setup 安装脚本
`
