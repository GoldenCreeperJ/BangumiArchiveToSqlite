import sqlite3
from util import Converter, CustomizedMigrator, StandardMigrator

if __name__ == '__main__':
    if input("Start the Conversion process?(Y/n)").strip().lower() in ["", "y", "yes"]:
        Converter.jsonl_to_json()

    if input("Start the Mapping process?(Y/n)").strip().lower() in ["", "y", "yes"]:
        Converter.yaml_to_json()

    if input("Start the SQLite migration process?(Y/n)").strip().lower() in ["", "y", "yes"]:
        sqlite_db_file = f'./output/{input("SQLite database file path (default: dump): ").strip() or "dump"}.db'
        match input('''Migration mode (default: Personal): \n1. Standard\n2. Mini\n3. Personal\n''').strip().lower():
            case "1" | "standard" | "s":
                migrator = StandardMigrator.StandardMigrator
            case "2" | "mini" | "m":
                migrator = CustomizedMigrator.MiniMigrator
            case "3" | "personal" | "p" | "":
                migrator = CustomizedMigrator.PersonalMigrator
            case _:
                print("Invalid migration mode, exiting...")
                exit()

        with sqlite3.connect(sqlite_db_file) as conn:
            cursor = conn.cursor()
            migrator.insert(conn, cursor, migrator)
