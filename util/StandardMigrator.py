import json
import util.Converter as Converter


class StandardMigrator:
    @staticmethod
    def migrate_table(conn, table_name, columns, process_row, default_columns=None):
        temp_table = f"temp_{table_name}"
        old_table = f"old_{table_name}"

        indexes_sql = []
        if conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)).fetchone():
            rows = conn.execute(f"SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=? AND sql IS NOT NULL",(table_name,)).fetchall()
            indexes_sql = [sql[0].replace(table_name, temp_table) for sql in rows]

        create_sql = f"CREATE TABLE IF NOT EXISTS {temp_table} ({', '.join(columns)});"
        conn.executescript(create_sql + "\n" + ";\n".join(indexes_sql))

        batch = []
        with (open(f"./input/{'-'.join(table_name.split('_'))}.jsonlines", 'r', encoding='utf-8') as f):
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    item = process_row(json.loads(line))
                except json.JSONDecodeError: continue

                if not item: continue
                batch.append(item)

                if len(batch) >= 5000:
                    with conn:
                        conn.executemany(f"INSERT INTO {temp_table} VALUES ({','.join(['?'] * len(batch[0]))})",batch)
                    batch.clear()

            if batch:
                with conn:
                    conn.executemany(f"INSERT INTO {temp_table} VALUES ({','.join(['?'] * len(batch[0]))})",batch)

        if default_columns and len(default_columns) > 1:
            update_cols = ", ".join([f"{col} = old_t.{col}" for col in default_columns[1:]])
            conn.execute(f"""UPDATE {temp_table} AS new_t SET {update_cols} 
                FROM {table_name} AS old_t WHERE new_t.{default_columns[0]} = old_t.{default_columns[0]}""")

        with conn:
            if conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)).fetchone():
                conn.execute(f"ALTER TABLE {table_name} RENAME TO {old_table}")
            conn.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
            conn.execute(f"DROP TABLE IF EXISTS {old_table}")

    def insert_subject(self, conn):
        self.migrate_table(conn, 'subject', [
            'id INTEGER PRIMARY KEY',
            'type INTEGER',
            'name TEXT',
            'name_cn TEXT',
            'infobox TEXT',
            'platform INTEGER',
            'summary TEXT',
            'nsfw INTEGER',
            'tags TEXT',
            'meta_tags TEXT',
            'score REAL',
            'score_details TEXT',
            'rank INTEGER',
            'date TEXT',
            'favorite TEXT',
            'series INTEGER'
        ], lambda item: (item['id'],
                         item['type'],
                         item['name'],
                         item['name_cn'] or item['name'],
                         Converter.infoBox_to_json(item['infobox']),
                         item['platform'], item["summary"], item["nsfw"],
                         json.dumps(item["tags"], ensure_ascii=False),
                         json.dumps(item["meta_tags"], ensure_ascii=False),
                         item["score"],
                         json.dumps(item["score_details"], ensure_ascii=False),
                         item["rank"],
                         item["date"],
                         json.dumps(item["favorite"], ensure_ascii=False),
                         (1 if item["series"] else 0) if item['type'] == 1 else 2
                         ))

    def insert_character(self, conn):
        self.migrate_table(conn, 'character', [
            'id INTEGER PRIMARY KEY',
            'role INTEGER',
            'name TEXT',
            'infobox TEXT',
            'summary TEXT',
            'comments INTEGER',
            'collects INTEGER'
        ], lambda item: (item['id'],
                         item['role'],
                         item['name'],
                         Converter.infoBox_to_json(item['infobox']),
                         item["summary"],
                         item["comments"],
                         item["collects"]
                         ))

    def insert_person(self, conn):
        self.migrate_table(conn, 'person', [
            'id INTEGER PRIMARY KEY',
            'name TEXT',
            'type INTEGER',
            'career TEXT',
            'infobox TEXT',
            'summary TEXT',
            'comments INTEGER',
            'collects INTEGER'
        ], lambda item: (item['id'],
                         item['name'],
                         item['type'],
                         json.dumps(item['career'], ensure_ascii=False),
                         Converter.infoBox_to_json(item['infobox']),
                         item["summary"],
                         item["comments"],
                         item["collects"]
                         ))

    def insert_episode(self, conn):
        self.migrate_table(conn, 'episode', [
            'id INTEGER PRIMARY KEY',
            'name TEXT',
            'name_cn TEXT',
            'description TEXT',
            'airdate TEXT',
            'disc INTEGER',
            'duration TEXT',
            'subject_id INTEGER',
            'sort INTEGER',
            'type INTEGER',
            'FOREIGN KEY (subject_id) REFERENCES subject(id)'
        ], lambda item: (item['id'],
                         item['name'],
                         item.get('name_cn', item['name']),
                         item['description'],
                         item['airdate'],
                         item['disc'],
                         item['duration'],
                         item['subject_id'],
                         item["sort"],
                         item['type']
                         ))

    def insert_person_character(self, conn):
        self.migrate_table(conn, 'person_characters', [
            'person_id INTEGER',
            'subject_id INTEGER',
            'character_id INTEGER',
            'summary TEXT',
            'FOREIGN KEY(person_id) REFERENCES person(id)',
            'FOREIGN KEY(subject_id) REFERENCES subject(id)',
            'FOREIGN KEY (character_id) REFERENCES character(id)'
        ], lambda item: (item['person_id'],
                         item['subject_id'],
                         item['character_id'],
                         item['summary']
                         ))

    def insert_subject_character(self, conn):
        self.migrate_table(conn, 'subject_characters', [
            'character_id INTEGER',
            'subject_id INTEGER',
            'type INTEGER',
            '"order" INTEGER',
            'FOREIGN KEY (character_id) REFERENCES character(id)',
            'FOREIGN KEY (subject_id) REFERENCES subject(id)'
        ], lambda item: (item['character_id'],
                         item['subject_id'],
                         item['type'],
                         item['order']
                         ))

    def insert_subject_person(self, conn):
        self.migrate_table(conn, 'subject_persons', [
            'person_id INTEGER',
            'subject_id INTEGER',
            'position INTEGER',
            'appear_eps TEXT',
            'FOREIGN KEY (person_id) REFERENCES person(id)',
            'FOREIGN KEY (subject_id) REFERENCES subject(id)'
        ], lambda item: (item['person_id'],
                         item['subject_id'],
                         item['position'],
                         item['appear_eps']
                         ))

    def insert_subject_relation(self, conn):
        self.migrate_table(conn, 'subject_relations', [
            'subject_id INTEGER',
            'relation_type INTEGER',
            'related_subject_id INTEGER',
            '"order" INTEGER',
            'FOREIGN KEY(subject_id) REFERENCES subject(id)',
            'FOREIGN KEY(related_subject_id) REFERENCES subject(id)'
        ], lambda item: (item['subject_id'],
                         item['relation_type'],
                         item['related_subject_id'],
                         item['order']
                         ))

    def insert_person_relation(self, conn):
        self.migrate_table(conn, 'person_relations', [
            'person_type TEXT',
            'person_id INTEGER',
            'related_person_id INTEGER',
            'relation_type INTEGER',
            'spoiler INTEGER',
            'ended INTEGER',
            'FOREIGN KEY(person_id) REFERENCES person(id)',
            'FOREIGN KEY(related_person_id) REFERENCES person(id)'
            ], lambda item: (item['person_type'],
                             item['person_id'],
                             item['related_person_id'],
                             item['relation_type'],
                             item['spoiler'],
                             item['ended']
                             )
        )

    def insert(self, conn):
        """执行全量数据迁移"""
        self.insert_subject(conn)
        print("主作品表创建完成")
        self.insert_character(conn)
        print("角色表创建完成")
        self.insert_person(conn)
        print("人物表创建完成")
        self.insert_episode(conn)
        print("剧集表创建完成")
        self.insert_person_character(conn)
        print("人物-角色关联表创建完成")
        self.insert_subject_character(conn)
        print("作品-角色关联表创建完成")
        self.insert_subject_person(conn)
        print("作品-人员关联表创建完成")
        self.insert_subject_relation(conn)
        print("作品-关联作品表创建完成")
        self.insert_person_relation(conn)
        print("人物-关联人物表创建完成")

        print("\n所有数据表创建完成\n")
