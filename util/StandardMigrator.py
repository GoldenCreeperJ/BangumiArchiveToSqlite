import json
import util.Converter as Converter


class StandardMigrator:
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
                tags TEXT,
                meta_tags TEXT,
                score REAL,
                score_details TEXT,
                rank INTEGER,
                date TEXT,
                favorite TEXT,
                series INTEGER)''')
        cursor.execute('''DELETE FROM subject; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/subject.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO subject(id, type, name, name_cn, infobox, platform, summary, nsfw, tags, meta_tags, score, 
                    score_details,rank, date, favorite, series) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                               item['id'], item['type'], item['name'], item['name_cn'] if item['name_cn'] else item['name'],
                               Converter.infoBox_to_json(item['infobox']), item['platform'], item["summary"], item["nsfw"],
                               json.dumps(item["tags"], ensure_ascii=False), json.dumps(item["meta_tags"], ensure_ascii=False),
                               item["score"], json.dumps(item["score_details"], ensure_ascii=False), item["rank"],
                               item["date"], json.dumps(item["favorite"], ensure_ascii=False),
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
                summary TEXT,
                comments INTEGER,
                collects INTEGER)''')
        cursor.execute('''DELETE FROM character; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/character.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO character(id, role,name,infobox,summary,comments,collects) VALUES (?,?,?,?,?,?,?)''',
                               (item['id'], item['role'], item['name'], Converter.infoBox_to_json(item['infobox']),
                                item["summary"], item["comments"], item["collects"]))
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
                summary TEXT,
                comments INTEGER,
                collects INTEGER)''')
        cursor.execute('''DELETE FROM person; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/person.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO person(id,name,type,career,infobox,summary,comments,collects) VALUES (?,?,?,?,?,?,?,?)''',
                               (item['id'], item['name'], item['type'], json.dumps(item['career'], ensure_ascii=False),
                                Converter.infoBox_to_json(item['infobox']), item["summary"], item["comments"], item["collects"]))
        conn.commit()

    @staticmethod
    def insert_person_character(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS person_character (
                person_id INTEGER,
                subject_id INTEGER,
                character_id INTEGER,
                summary TEXT,
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
                    INSERT INTO person_character(person_id,subject_id,character_id,summary) VALUES (?,?,?,?)''',
                               (item["person_id"], item["subject_id"], item["character_id"], item["summary"]))
        conn.commit()

    @staticmethod
    def insert_episode(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episode(
                id INTEGER PRIMARY KEY,
                name TEXT,
                name_cn TEXT,
                description TEXT,
                airdate TEXT,
                disc INTEGER,
                duration TEXT,
                subject_id INTEGER,
                sort INTEGER,
                type INTEGER,
                FOREIGN KEY (subject_id) REFERENCES subject(id))''')
        cursor.execute('''DELETE FROM episode; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/episode.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO episode(id,name,name_cn,description,airdate,disc,duration,subject_id,sort,type) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                               (item['id'], item['name'], item['name_cn'] if item['name_cn'] else item['name'],
                                item['description'], item['airdate'], item['disc'], item['duration'],
                                item['subject_id'],
                                item["sort"], item['type']))
        conn.commit()

    @staticmethod
    def insert_subject_character(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subject_character (
                character_id INTEGER,
                subject_id INTEGER,
                type INTEGER,
                "order" INTEGER,
                FOREIGN KEY (character_id) REFERENCES character(id),
                FOREIGN KEY (subject_id) REFERENCES subject(id))''')
        cursor.execute('''DELETE FROM subject_character; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/subject-characters.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO subject_character(character_id,subject_id, type, "order") VALUES (?,?,?,?)''',
                               (item["character_id"], item["subject_id"], item["type"], item["order"]))
        conn.commit()

    @staticmethod
    def insert_subject_person(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subject_person (
                person_id INTEGER,
                subject_id INTEGER,
                position INTEGER,
                FOREIGN KEY (person_id) REFERENCES person(id),
                FOREIGN KEY (subject_id) REFERENCES subject(id))''')
        cursor.execute('''DELETE FROM subject_person; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/subject-persons.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO subject_person(person_id,subject_id, position) VALUES (?,?,?)''',
                               (item["person_id"], item["subject_id"], item["position"]))
        conn.commit()

    @staticmethod
    def insert_subject_relation(conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subject_relation (
                subject_id INTEGER,
                relation_type INTEGER,
                related_subject_id INTEGER,
                "order" INTEGER,
                FOREIGN KEY (subject_id) REFERENCES subject(id),
                FOREIGN KEY (related_subject_id) REFERENCES subject(id))''')
        cursor.execute('''DELETE FROM subject_relation; ''')
        conn.commit()
        cursor.execute('''VACUUM;''')

        with open("./input/subject-relations.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())

                cursor.execute('''
                    INSERT INTO subject_relation(subject_id, relation_type, related_subject_id, "order") VALUES (?,?,?,?)''',
                               (item["subject_id"], item["relation_type"], item["related_subject_id"],
                                item["order"]))
        conn.commit()

    @staticmethod
    def insert(conn, cursor, migrator):
        migrator.insert_subject(conn, cursor)
        print("Subject table created")
        migrator.insert_character(conn, cursor)
        print("Character table created")
        migrator.insert_person(conn, cursor)
        print("Person table created")
        migrator.insert_person_character(conn, cursor)
        print("Person-Character table created")
        migrator.insert_episode(conn, cursor)
        print("Episode table created")
        migrator.insert_subject_character(conn, cursor)
        print("Subject-Character table created")
        migrator.insert_subject_person(conn, cursor)
        print("Subject-Person table created")
        migrator.insert_subject_relation(conn, cursor)
        print("Subject-Relation table created")

        print("\nAll tables created\n")
