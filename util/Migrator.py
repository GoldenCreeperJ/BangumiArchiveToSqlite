import json
import util.Converter as Converter


def insert_subject(conn, cursor, input_path):
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
            series INTEGER,
            rating INTEGER,
            status INTEGER)''')
    cursor.execute("SELECT id,rating,status FROM subject")
    rows = {i[0]: (i[1], i[2]) for i in cursor.fetchall()}
    cursor.execute('''DELETE FROM subject; ''')
    conn.commit()
    cursor.execute('''VACUUM;''')

    with open(input_path + "subject.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO subject(id, type, name, name_cn, infobox, platform, summary, nsfw, tags, meta_tags, score, 
                score_details,rank, date, favorite, series, rating, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                           item['id'], item['type'], item['name'], item['name_cn'] if item['name_cn'] else item['name'],
                           Converter.infoBox_to_json(item['infobox']), item['platform'], item["summary"], item["nsfw"],
                           json.dumps(item["tags"], ensure_ascii=False), json.dumps(item["meta_tags"], ensure_ascii=False),
                           item["score"], json.dumps(item["score_details"], ensure_ascii=False), item["rank"],
                           item["date"], json.dumps(item["favorite"], ensure_ascii=False),
                           (1 if item["series"] else 0) if item[type] == 1 else 2,
                           rows.get(int(item['id']), [0])[0], rows.get(int(item['id']), [0, 0])[1]))

            conn.commit()

    print("Subject table created successfully")


def insert_character(conn, cursor, input_path):
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

    with open(input_path + "character.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO character(id, role,name,infobox,summary,comments,collects) VALUES (?,?,?,?,?,?,?)''',
                           (item['id'], item['role'], item['name'], Converter.infoBox_to_json(item['infobox']),
                            item["summary"], item["comments"], item["collects"]))
    conn.commit()

    print("Character table created successfully")


def insert_person(conn, cursor, input_path):
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

    with open(input_path + "person.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO person(id,name,type,career,infobox,summary,comments,collects) VALUES (?,?,?,?,?,?,?,?)''',
                           (item['id'], item['name'], item['type'], json.dumps(item['career'], ensure_ascii=False),
                            Converter.infoBox_to_json(item['infobox']), item["summary"], item["comments"],
                            item["collects"]))
    conn.commit()

    print("Person table created successfully")


def insert_episode(conn, cursor, input_path):
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

    with open(input_path + "episode.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO episode(id,name,name_cn,description,airdate,disc,duration,subject_id,sort,type) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                           (item['id'], item['name'], item['name_cn'] if item['name_cn'] else item['name'],
                            item['description'], item['airdate'], item['disc'], item['duration'], item['subject_id'],
                            item["sort"], item['type']))
    conn.commit()

    print("Episode table created successfully")


def insert_subject_character(conn, cursor, input_path):
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

    with open(input_path + "subject-characters.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO subject_character(character_id,subject_id, type, "order") VALUES (?,?,?,?)''',
                           (item["character_id"], item["subject_id"], item["type"], item["order"]))
    conn.commit()

    print("Subject-Character table created successfully")


def insert_subject_person(conn, cursor, input_path):
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

    with open(input_path + "subject-persons.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO subject_person(person_id,subject_id, position) VALUES (?,?,?)''',
                           (item["person_id"], item["subject_id"], item["position"]))
    conn.commit()

    print("Subject-Person table created successfully")


def insert_subject_relation(conn, cursor, input_path):
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

    with open(input_path + "subject-relations.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO subject_relation(subject_id, relation_type, related_subject_id, "order") VALUES (?,?,?,?)''',
                           (item["subject_id"], item["relation_type"], item["related_subject_id"], item["order"]))
    conn.commit()

    print("Subject-Relation table created successfully")


def insert_person_character(conn, cursor, input_path):
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

    with open(input_path + "person-characters.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO person_character(person_id,subject_id,character_id) VALUES (?,?,?)''',
                           (item["person_id"], item["subject_id"], item["character_id"]))
    conn.commit()

    print("Person-Character table created successfully")
