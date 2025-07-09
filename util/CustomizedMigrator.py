import json
import util.Converter as Converter
from util import StandardMigrator


class MiniMigrator(StandardMigrator.StandardMigrator):
    def insert_subject(self, conn):
        self.migrate_table(conn, 'subject', (
            'id INTEGER PRIMARY KEY',
            'type INTEGER',
            'name TEXT',
            'name_cn TEXT',
            'infobox TEXT',
            'platform INTEGER',
            'summary TEXT',
            'nsfw INTEGER',
            'meta_tags TEXT',
            'date TEXT',
            'series INTEGER'
        ), lambda item: (
            item['id'],
            item['type'],
            item['name'],
            item.get('name_cn', item['name']),
            Converter.infoBox_to_json(item['infobox']),
            item['platform'],
            item["summary"],
            int(item["nsfw"]),
            json.dumps(item["meta_tags"], ensure_ascii=False),
            item["date"],
            (1 if item.get("series") else 0) if item['type'] == 1 else 2
        ))

    def insert_character(self, conn):
        self.migrate_table(conn, 'character', (
            'id INTEGER PRIMARY KEY',
            'role INTEGER',
            'name TEXT',
            'infobox TEXT',
            'summary TEXT'
        ), lambda item: (
            item['id'],
            item['role'],
            item['name'],
            Converter.infoBox_to_json(item['infobox']),
            item["summary"]
        ))

    def insert_person(self, conn):
        self.migrate_table(conn, 'person', (
            'id INTEGER PRIMARY KEY',
            'name TEXT',
            'type INTEGER',
            'career TEXT',
            'infobox TEXT',
            'summary TEXT'
        ), lambda item: (
            item['id'],
            item['name'],
            item['type'],
            json.dumps(item['career'], ensure_ascii=False),
            Converter.infoBox_to_json(item['infobox']),
            item["summary"]
        ))

    def insert_person_character(self, conn):
        self.migrate_table(conn, 'person_characters', (
            'person_id INTEGER',
            'subject_id INTEGER',
            'character_id INTEGER',
            'FOREIGN KEY (person_id) REFERENCES person(id)',
            'FOREIGN KEY (subject_id) REFERENCES subject(id)',
            'FOREIGN KEY (character_id) REFERENCES character(id)'
        ), lambda item: (
            item['person_id'],
            item['subject_id'],
            item['character_id']
        ))


class PersonalMigrator(MiniMigrator):
    def insert_subject(self, conn):
        self.migrate_table(conn, 'subject', (
            'id INTEGER PRIMARY KEY',
            'type INTEGER',
            'name TEXT',
            'name_cn TEXT',
            'infobox TEXT',
            'platform INTEGER',
            'summary TEXT',
            'nsfw INTEGER',
            'meta_tags TEXT',
            'date TEXT',
            'series INTEGER',
            'rating INTEGER',
            'status INTEGER'
        ), lambda item: (
            item['id'],
            item['type'],
            item['name'],
            item.get('name_cn', item['name']),
            Converter.infoBox_to_json(item['infobox']),
            item['platform'],
            item["summary"],
            int(item["nsfw"]),
            json.dumps(item["meta_tags"], ensure_ascii=False),
            item["date"],
            (1 if item.get("series") else 0) if item['type'] == 1 else 2,
        ), ('id', 'rating', 'status'))


class AnimeMigrator(PersonalMigrator):
    def insert_subject(self, conn):
        self.migrate_table(conn, 'subject', (
            'id INTEGER PRIMARY KEY',
            'type INTEGER',
            'name TEXT',
            'name_cn TEXT',
            'infobox TEXT',
            'platform INTEGER',
            'summary TEXT',
            'nsfw INTEGER',
            'meta_tags TEXT',
            'date TEXT',
            'rating INTEGER',
            'status INTEGER'
        ), lambda item: (
            item['id'],
            item['type'],
            item['name'],
            item.get('name_cn', item['name']),
            Converter.infoBox_to_json(item['infobox']),
            item['platform'],
            item["summary"],
            int(item["nsfw"]),
            json.dumps(item["meta_tags"], ensure_ascii=False),
            item["date"]) if item['type'] == 2 else None,
                           ('id', 'rating', 'status'))

    def insert_episode(self, conn):
        return

    def insert_subject_episode(self, conn):
        return

    def insert_subject_relation(self, conn):
        return

    def insert_person(self, conn):
        return

    def insert_person_character(self, conn):
        return

    def insert_character(self, conn):
        return

    def insert_subject_character(self, conn):
        return

    def insert_subject_person(self, conn):
        return


class JapanAnimeMigrator(AnimeMigrator):
    def insert_subject(self, conn):
        self.migrate_table(conn, 'subject', (
            'id INTEGER PRIMARY KEY',
            'type INTEGER',
            'name TEXT',
            'name_cn TEXT',
            'infobox TEXT',
            'platform INTEGER',
            'summary TEXT',
            'nsfw INTEGER',
            'meta_tags TEXT',
            'date TEXT',
            'rating INTEGER',
            'status INTEGER'
        ), lambda item: (
            item['id'],
            item['type'],
            item['name'],
            item.get('name_cn', item['name']),
            Converter.infoBox_to_json(item['infobox']),
            item['platform'],
            item["summary"],
            int(item["nsfw"]),
            json.dumps(item["meta_tags"], ensure_ascii=False),
            item["date"]) if item['type'] == 2 and "日本" in item['meta_tags'] else None,
                           ('id', 'rating', 'status'))
