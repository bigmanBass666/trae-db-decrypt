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

| 表名 | 内容 |
|------|------|
| `history_v2` | 完整聊天内容（JSON 格式） |
| `chat_session` | 会话列表 |
| `agent` | Agent 定义（含 system prompt） |
| `agent_run` | Agent 运行记录 |
| `task` | 任务记录 |

## 参考项目

- [wechat-decrypt](https://github.com/ylytdeng/wechat-decrypt) - 微信数据库解密项目（主要参考）

## 许可证

MIT License
