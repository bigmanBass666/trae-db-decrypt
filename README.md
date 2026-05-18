# Trae CN Database Decryptor

> 🔓 从 Trae CN IDE 提取并解密 AI Agent 数据库

## 功能

- ✅ 从进程内存中提取 SQLCipher 密钥
- ✅ 支持 SQLCipher 4 数据库解密
- ✅ 导出完整的对话记录和 Agent 数据
- ✅ HMAC-SHA512 自动验证密钥正确性

## 快速开始

```bash
# 1. 确保 Trae CN 正在运行（需要 ai_agent.dll 加载）
# 2. 安装依赖（无需额外依赖，只用标准库）
# 3. 运行密钥扫描
python src/scan_memory.py

# 4. 使用提取的密钥读取数据库
python src/decrypt_db.py
```

## 项目结构

```
trae-db-decrypt/
├── README.md           # 本文件
├── src/
│   ├── scan_memory.py  # 密钥扫描脚本
│   └── decrypt_db.py   # 数据库解密工具
├── docs/
│   └── TRAEDB_GUIDE.md # 详细使用指南
└── examples/           # 示例代码
```

## 工作原理

1. **进程发现**：找到加载 `ai_agent.dll` 的 Trae CN 进程
2. **内存扫描**：用 Windows API 读取进程内存，搜索 hex 密钥模式
3. **密钥验证**：用 HMAC-SHA512 验证找到的密钥是否正确
4. **数据库解密**：使用验证过的密钥解密 SQLCipher 数据库

## 密钥格式

Trae CN 使用 SQLCipher 4 raw key 模式，密钥存储为：

```
x'<64hex_enc_key><32hex_salt>'
```

## 数据库表结构

### 核心对话表

| 表名 | 行数 | 内容说明 |
|------|------|----------|
| `history_v2` | 15,914 | **完整聊天内容**（JSON格式，包含用户消息和AI回复） |
| `chat_session` | 238 | 会话列表（含标题、类型、创建时间） |
| `chat_message` | 3,048 | 消息元数据（关联会话和消息） |
| `chat_turn` | 1,527 | 对话轮次（含agent类型、状态、引用） |

### Agent 相关表

| 表名 | 行数 | 内容说明 |
|------|------|----------|
| `agent` | 17 | Agent定义（含system prompt、描述、工具列表） |
| `agent_run` | 1,689 | Agent运行记录（含session、状态、token使用） |
| `agent_member_relation` | 28 | Agent成员关系 |

### 任务/项目表

| 表名 | 行数 | 内容说明 |
|------|------|----------|
| `task` | 1,424 | 任务记录（含session、状态、时间） |
| `project` | 23 | 项目信息（含路径、创建时间） |
| `todo_list` | 1,739 | 待办事项（JSON格式，含任务列表） |
| `history_todo_list` | 1,739 | 历史待办记录 |

### 配置/缓存表

| 表名 | 行数 | 内容说明 |
|------|------|----------|
| `server_history_info` | 32,692 | 服务器历史信息（含完整消息、工作区） |
| `session_project` | 238 | 会话-项目关联 |
| `model_config_cache` | 42 | 模型配置缓存 |
| `mcp_server_agent_relation` | 58 | MCP服务器-Agent关联 |
| `rules_attachment` | 744 | 规则附件 |
| `user_configuration` | 2 | 用户配置 |
| `multi_root_path` | 15 | 多根路径配置 |

### 系统表

| 表名 | 行数 | 内容说明 |
|------|------|----------|
| `migration_sql_store` | 70 | 数据库迁移SQL |
| `seaql_migrations` | 70 | SeaQL迁移记录 |
| `sqlite_sequence` | 20 | SQLite序列 |

### 重要发现

1. **`history_v2`** 是最重要的表，包含完整对话内容（JSON格式）
2. **`agent`** 表存储了所有自定义Agent的system prompt
3. **`todo_list`** 包含JSON格式的待办事项列表
4. **`server_history_info`** 有32,692行，包含服务器端的完整消息记录

## 参考项目

- [wechat-decrypt](https://github.com/ylytdeng/wechat-decrypt) - 微信数据库解密项目（主要参考）

## 许可证

MIT License
