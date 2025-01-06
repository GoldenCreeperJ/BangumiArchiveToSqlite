import json
import Converter


def insert_subject(conn, cursor, input_path, mapping_table):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject(
            id INTEGER PRIMARY KEY,
            type TEXT,
            name TEXT,
            name_cn TEXT,
            infobox TEXT,
            platform TEXT,
            summary TEXT,
            nsfw BOOLEAN,
            tags TEXT,
            score REAL,
            score_details TEXT,
            rank INTEGER,
            date TEXT,
            favorite TEXT,
            series TEXT)''')
    cursor.execute('''DELETE FROM subject; ''')
    cursor.execute('''VACUUM;''')

    with open(input_path + "subject.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO subject(id, type, name, name_cn, infobox, platform, summary, nsfw, tags, score, 
                score_details,rank, date, favorite, series) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           (item['id'], mapping_table["subject_types"][str(item['type'])], item['name'],
                            item['name_cn'] if item['name_cn'] else item['name'],
                            Converter.infoBox_to_json(item['infobox']),
                            mapping_table["subject_platforms"][str(item['type'])][str(item['platform'])],
                            item["summary"], item["nsfw"], json.dumps(item["tags"]), item["score"],
                            json.dumps(item["score_details"]), item["rank"], item["date"], json.dumps(item["favorite"]),
                            mapping_table["book_series"]["1" if item["series"] else "0"] if item['type'] == 1 else ""))
    conn.commit()


def insert_character(conn, cursor, input_path, mapping_table):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS character(
            id INTEGER PRIMARY KEY,
            role TEXT,
            name TEXT,
            infobox TEXT,
            summary TEXT,
            comments INTEGER,
            collects INTEGER)''')
    cursor.execute('''DELETE FROM character; ''')
    cursor.execute('''VACUUM;''')

    with open(input_path + "character.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO character(id, role,name,infobox,summary,comments,collects) VALUES (?,?,?,?,?,?,?)''',
                           (item['id'], mapping_table["character_role"][str(item['role'])], item['name'],
                            Converter.infoBox_to_json(item['infobox']), item["summary"], item["comments"],
                            item["collects"]))
    conn.commit()


def insert_person(conn, cursor, input_path, mapping_table):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS person(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            career TEXT,
            infobox TEXT,
            summary TEXT,
            comments INTEGER,
            collects INTEGER)''')
    cursor.execute('''DELETE FROM person; ''')
    cursor.execute('''VACUUM;''')

    with open(input_path + "person.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO person(id,name,type,career,infobox,summary,comments,collects) VALUES (?,?,?,?,?,?,?,?)''',
                           (item['id'], item['name'], mapping_table["person_types"][str(item['type'])],
                            json.dumps(item['career']), Converter.infoBox_to_json(item['infobox']),
                            item["summary"], item["comments"], item["collects"]))
    conn.commit()


def insert_episode(conn, cursor, input_path, mapping_table):
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
            type TEXT)''')
    cursor.execute('''DELETE FROM episode; ''')
    cursor.execute('''VACUUM;''')

    with open(input_path + "episode.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO episode(id,name,name_cn,description,airdate,disc,duration,subject_id,sort,type) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                           (item['id'], item['name'], item['name_cn'] if item['name_cn'] else item['name'],
                            item['description'], item['airdate'], item['disc'], item['duration'], item['subject_id'],
                            item["sort"], mapping_table["episode_types"][str(item['type'])]))
    conn.commit()


def insert_subject_character(conn, cursor, input_path, mapping_table):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject_character (
            character_id INTEGER,
            subject_id INTEGER,
            type TEXT,
            "order" INTEGER)''')
    cursor.execute('''DELETE FROM subject_character; ''')
    cursor.execute('''VACUUM;''')

    with open(input_path + "subject-characters.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO subject_character(character_id,subject_id, type, "order") VALUES (?,?,?,?)''',
                           (item["character_id"], item["subject_id"],
                            mapping_table["character_types"][str(item["type"])], item["order"]))
    conn.commit()


def insert_subject_person(conn, cursor, input_path, mapping_table):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject_person (
            person_id INTEGER,
            subject_id INTEGER,
            position TEXT)''')
    cursor.execute('''DELETE FROM subject_person; ''')
    cursor.execute('''VACUUM;''')

    with open(input_path + "subject-persons.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO subject_person(person_id,subject_id, position) VALUES (?,?,?)''',
                           (item["person_id"], item["subject_id"],
                            mapping_table["subject_staffs"][str(item["position"])]))
    conn.commit()


def insert_subject_relation(conn, cursor, input_path, mapping_table):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject_relation (
            subject_id INTEGER,
            relation_type TEXT,
            related_subject_id INTEGER,
            "order" INTEGER)''')
    cursor.execute('''DELETE FROM subject_relation; ''')
    cursor.execute('''VACUUM;''')

    with open(input_path + "subject-relations.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO subject_relation(subject_id, relation_type, related_subject_id, "order") VALUES (?,?,?,?)''',
                           (item["subject_id"], mapping_table["subject_relations"][str(item["relation_type"])],
                            item["related_subject_id"], item["order"]))
    conn.commit()


def insert_person_character(conn, cursor, input_path):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS person_character (
            person_id INTEGER,
            subject_id INTEGER,
            character_id INTEGER,
            summary TEXT)''')
    cursor.execute('''DELETE FROM person_character; ''')
    cursor.execute('''VACUUM;''')

    with open(input_path + "person-characters.jsonlines", 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line.strip())

            cursor.execute('''
                INSERT INTO person_character(person_id,subject_id,character_id, summary) VALUES (?,?,?,?)''',
                           (item["person_id"], item["subject_id"], item["character_id"], item["summary"]))
    conn.commit()

