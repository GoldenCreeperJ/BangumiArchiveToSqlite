import json
import util.Converter as Converter


class StandardMigrator:
    @staticmethod
    def migrate_table(conn, table_name, columns, process_row, default_columns=None):
        batch, rows = [], {}
        conn.executescript(f'''
            CREATE TABLE IF NOT EXISTS {table_name}({', '.join(columns)});
            CREATE TABLE temp_{table_name}({', '.join(columns)});
            ''')
        if default_columns:
            rows = {i[0]: i[1:] for i in conn.execute(f"SELECT {','.join(default_columns)} FROM {table_name}")}
        with (open(f"./input/{'-'.join(table_name.split('_'))}.jsonlines", 'r', encoding='utf-8') as f):
            for line in f:
                item = process_row(json.loads(line.strip()))
                if item:
                    if default_columns:
                        item += rows.get(item[0], tuple(0 for _ in range(len(default_columns) - 1)))
                    batch.append(item)
                    if len(batch) >= 5000:
                        conn.executemany(
                            f'''INSERT INTO temp_{table_name} VALUES ({','.join(['?'] * len(batch[0]))})''', batch)
                        batch.clear()
            if batch:
                conn.executemany(f'''INSERT INTO temp_{table_name} VALUES ({','.join(['?'] * len(batch[0]))})''', batch)
        with conn:
            conn.execute(f"ALTER TABLE {table_name} RENAME TO old_{table_name}")
            conn.execute(f"ALTER TABLE temp_{table_name} RENAME TO {table_name}")
            conn.execute(f"DROP TABLE IF EXISTS old_{table_name}")

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
            'FOREIGN KEY (person_id) REFERENCES person(id)',
            'FOREIGN KEY (subject_id) REFERENCES subject(id)'
        ], lambda item: (item['person_id'],
                         item['subject_id'],
                         item['position']
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

        print("\n所有数据表创建完成\n")
