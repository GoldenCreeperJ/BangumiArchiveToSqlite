import sqlite3
from util import Converter, CustomizedMigrator, StandardMigrator

if __name__ == '__main__':
    if input("开始转换流程? (Y/n)").strip().lower() in ["", "y", "yes"]:
        Converter.jsonl_to_json()

    if input("开始映射流程? (Y/n)").strip().lower() in ["", "y", "yes"]:
        Converter.yaml_to_json()

    if input("开始SQLite迁移流程? (Y/n)").strip().lower() in ["", "y", "yes"]:
        sqlite_db_file = f'./output/{input("SQLite数据库文件路径(默认: dump): ").strip() or "dump"}.db'
        match input('''迁移模式选择(默认: Personal): \n1. Standard\n2. Mini\n3. Personal\n4. Anime\n5. JapanAnime\n''').strip().lower():
            case "1" | "standard" | "s":
                migrator = StandardMigrator.StandardMigrator()
            case "2" | "mini" | "m":
                migrator = CustomizedMigrator.MiniMigrator()
            case "3" | "personal" | "p" | "":
                migrator = CustomizedMigrator.PersonalMigrator()
            case "4" | "anime" | "a":
                migrator = CustomizedMigrator.AnimeMigrator()
            case "5" | "japanAnime" | "ja":
                migrator = CustomizedMigrator.JapanAnimeMigrator()
            case _:
                print("无效的迁移模式，程序终止...")
                exit()

        with sqlite3.connect(sqlite_db_file) as conn:
            conn.executescript('''
                PRAGMA temp_store=MEMORY;
                PRAGMA journal_mode=WAL;
                PRAGMA page_size=8192;
                PRAGMA cache_size=-250000;
                PRAGMA mmap_size=268435456;
                PRAGMA auto_vacuum=FULL;
            ''')
            migrator.insert(conn)
            conn.executescript('''
                PRAGMA wal_autocheckpoint=4000;
                PRAGMA foreign_keys = ON;
                PRAGMA foreign_key_check;
                PRAGMA integrity_check;
                PRAGMA optimize;
            ''')
