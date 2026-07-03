# OpenXterm 开发计划

## Phase 1: 项目初始化
1. [x] 创建项目目录结构
2. [ ] 安装依赖：pip install cryptography pyinstaller

## Phase 2: 核心模块
3. [ ] 实现数据库模块（db.py）：SQLite 建表、CRUD
4. [ ] 实现加密模块（crypto.py）：Fernet 密码加解密
5. [ ] 实现 SSH 命令解析模块（parser.py）：从命令字符串提取连接参数

## Phase 3: GUI 界面
6. [ ] 实现主窗口（main.py）：Tkinter 界面
7. [ ] 实现连接列表视图
8. [ ] 实现新建/编辑连接对话框（含密码小眼睛）
9. [ ] 实现一键连接功能

## Phase 4: 打包与发布
10. [ ] 编写 build_exe.py（PyInstaller 打包脚本）
11. [ ] 构建 exe 安装包
12. [ ] 测试安装与运行

## Phase 5: 验收
13. [ ] 对照 check.md 逐项验证
