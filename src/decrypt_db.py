"""
Trae CN 数据库解密工具
使用提取的密钥解密 SQLCipher 数据库
"""
import sqlite3
import sys
import os

def decrypt_database(db_path, key):
    """解密并读取数据库"""
    if not os.path.exists(db_path):
        print(f"[!] Database not found: {db_path}")
        return None
    
    # 确保密钥格式正确
    if not key.startswith("x'"):
        key = f"x'{key}'"
    if not key.endswith("'"):
        key = f"{key}'"
    
    try:
        db = sqlite3.connect(db_path)
        db.execute(f"PRAGMA key = '{key}'")
        
        # 测试连接
        result = db.execute("SELECT count(*) FROM sqlite_master").fetchone()
        if result:
            print(f"[+] Database decrypted successfully!")
            print(f"[+] Found {result[0]} tables")
            return db
        else:
            print("[!] Failed to decrypt database")
            db.close()
            return None
    except Exception as e:
        print(f"[!] Error: {e}")
        return None

def list_tables(db):
    """列出所有表"""
    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    print(f"\n[=] Tables ({len(tables)}):")
    for t in tables:
        count = db.execute(f"SELECT count(*) FROM [{t[0]}]").fetchone()[0]
        print(f"  - {t[0]}: {count} rows")

def export_sessions(db, output_file="sessions.json"):
    """导出会话数据"""
    import json
    
    sessions = db.execute("""
        SELECT s.session_id, s.session_title, s.session_type,
               s.created_at, s.updated_at
        FROM chat_session s
        ORDER BY s.created_at DESC
    """).fetchall()
    
    result = []
    for s in sessions:
        # 获取该会话的历史记录
        history = db.execute("""
            SELECT messages, agent_type, token_usage, created_at
            FROM history_v2
            WHERE session_id = ?
            ORDER BY created_at
        """, (s[0],)).fetchall()
        
        messages = []
        for h in history:
            if h[0]:
                try:
                    msg_data = json.loads(h[0])
                    if 'raw_messages' in msg_data:
                        for msg in msg_data['raw_messages']:
                            role = msg.get('role', '')
                            content = msg.get('content', [])
                            text = ' '.join([p.get('text', '') for p in content if p.get('type') == 'text'])
                            if text:
                                messages.append({
                                    'role': role,
                                    'content': text,
                                    'agent_type': h[1],
                                    'timestamp': h[3]
                                })
                except:
                    pass
        
        result.append({
            'session_id': s[0],
            'title': s[1],
            'type': s[2],
            'created_at': s[3],
            'messages': messages
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"[+] Exported {len(result)} sessions to {output_file}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python decrypt_db.py <database.db> <key>")
        print("")
        print("Example:")
        print('  python decrypt_db.py database.db "x\'3605...\'"')
        sys.exit(1)
    
    db_path = sys.argv[1]
    key = sys.argv[2]
    
    db = decrypt_database(db_path, key)
    if db:
        list_tables(db)
        
        # 询问是否导出
        response = input("\nExport sessions to JSON? (y/n): ")
        if response.lower() == 'y':
            export_sessions(db)
        
        db.close()

if __name__ == "__main__":
    main()
