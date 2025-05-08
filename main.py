import sqlite3
from util.Migrator import *

input_path = './input/'
output_path = './output/'
sqlite_db_file = './dump.db'

Converter.jsonl_to_json(input_path + "subject.jsonlines", output_path + "subject.json")
Converter.jsonl_to_json(input_path + "person.jsonlines", output_path + "person.json")
Converter.jsonl_to_json(input_path + "episode.jsonlines", output_path + "episode.json")
Converter.jsonl_to_json(input_path + "character.jsonlines", output_path + "character.json")
Converter.jsonl_to_json(input_path + "subject-persons.jsonlines", output_path + "subject_person.json")
Converter.jsonl_to_json(input_path + "subject-characters.jsonlines", output_path + "subject_character.json")
Converter.jsonl_to_json(input_path + "subject-relations.jsonlines", output_path + "subject_relation.json")
Converter.jsonl_to_json(input_path + "person-characters.jsonlines", output_path + "person_character.json")
Converter.yaml_to_json("./input", "./util/MappingTable.json")

print("\nJSON files created successfully\n")

conn = sqlite3.connect(sqlite_db_file)
cursor = conn.cursor()

insert_subject(conn, cursor, input_path)
insert_person(conn, cursor, input_path)
insert_episode(conn, cursor, input_path)
insert_character(conn, cursor, input_path)
insert_subject_person(conn, cursor, input_path)
insert_subject_character(conn, cursor, input_path)
insert_subject_relation(conn, cursor, input_path)
insert_person_character(conn, cursor, input_path)

conn.close()

print("\nAll tables created successfully\n")
