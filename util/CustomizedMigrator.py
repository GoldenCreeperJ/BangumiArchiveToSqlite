import json
import util.Converter as Converter
from util import StandardMigrator


class MiniMigrator(StandardMigrator.StandardMigrator):
    @staticmethod
    def insert_subject(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subject(
                id INTEGER PRIMARY KEY,
                type INTEGER,
                name TEXT,
                name_cn TEXT,
                infobox TEXT,
                platform INTEGER,
                summary TEXT,
                nsfw BOOLEAN,
                meta_tags TEXT,
                date TEXT,
                series INTEGER)''')
        cursor.execute('''DELETE FROM subject; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/subject.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO subject(id, type, name, name_cn, infobox, platform, summary, nsfw, meta_tags, date, series) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (
                               item['id'], item['type'], item['name'], item['name_cn'] if item['name_cn'] else item['name'],
                               Converter.infoBox_to_json(item['infobox']), item['platform'], item["summary"], item["nsfw"],
                               json.dumps(item["meta_tags"], ensure_ascii=False),item["date"],
                               (1 if item["series"] else 0) if item['type'] == 1 else 2))

                conn.commit()

    @staticmethod
    def insert_character(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character(
                id INTEGER PRIMARY KEY,
                role INTEGER,
                name TEXT,
                infobox TEXT,
                summary TEXT)''')
        cursor.execute('''DELETE FROM character; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/character.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO character(id, role,name,infobox,summary) VALUES (?,?,?,?,?)''',
                               (item['id'], item['role'], item['name'], Converter.infoBox_to_json(item['infobox']), item["summary"]))
        conn.commit()

    @staticmethod
    def insert_person(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS person(
                id INTEGER PRIMARY KEY,
                name TEXT,
                type INTEGER,
                career TEXT,
                infobox TEXT,
                summary TEXT)''')
        cursor.execute('''DELETE FROM person; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/person.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO person(id,name,type,career,infobox,summary) VALUES (?,?,?,?,?,?)''',
                               (item['id'], item['name'], item['type'], json.dumps(item['career'], ensure_ascii=False),
                                Converter.infoBox_to_json(item['infobox']), item["summary"]))
        conn.commit()

    @staticmethod
    def insert_person_character(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS person_character (
                person_id INTEGER,
                subject_id INTEGER,
                character_id INTEGER,
                FOREIGN KEY (person_id) REFERENCES person(id),
                FOREIGN KEY (subject_id) REFERENCES subject(id),
                FOREIGN KEY (character_id) REFERENCES character(id))''')
        cursor.execute('''DELETE FROM person_character; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/person-characters.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO person_character(person_id,subject_id,character_id) VALUES (?,?,?)''',
                               (item["person_id"], item["subject_id"], item["character_id"]))
        conn.commit()


class PersonalMigrator(MiniMigrator):
    @staticmethod
    def insert_subject(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subject(
                id INTEGER PRIMARY KEY,
                type INTEGER,
                name TEXT,
                name_cn TEXT,
                infobox TEXT,
                platform INTEGER,
                summary TEXT,
                nsfw BOOLEAN,
                meta_tags TEXT,
                date TEXT,
                series INTEGER,
                rating INTEGER,
                status INTEGER)''')
        cursor.execute("SELECT id,rating,status FROM subject")
        rows = {i[0]: (i[1], i[2]) for i in cursor.fetchall()}
        cursor.execute('''DELETE FROM subject; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/subject.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO subject(id, type, name, name_cn, infobox, platform, summary, nsfw, 
                    meta_tags, date, series, rating, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                               item['id'], item['type'], item['name'], item['name_cn'] if item['name_cn'] else item['name'],
                               Converter.infoBox_to_json(item['infobox']), item['platform'], item["summary"], item["nsfw"],
                               json.dumps(item["meta_tags"], ensure_ascii=False),item["date"],
                               (1 if item["series"] else 0) if item['type'] == 1 else 2,
                               rows.get(int(item['id']), [0])[0], rows.get(int(item['id']), [0, 0])[1]))

                conn.commit()
