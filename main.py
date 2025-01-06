import sqlite3
from util.Migrator import *

input_path = './input/'
output_path = './output/'
sqlite_db_file = './dump.db'

# Converter.yaml_to_json("./input","./MappingTable.json")
with open("MappingTable.json", "r", encoding="utf-8") as f:
    mapping_table = json.load(f)

conn = sqlite3.connect(sqlite_db_file)
cursor = conn.cursor()

insert_subject(conn, cursor, input_path, mapping_table)
insert_person(conn, cursor, input_path, mapping_table)
insert_episode(conn, cursor, input_path, mapping_table)
insert_character(conn, cursor, input_path, mapping_table)
insert_subject_person(conn, cursor, input_path, mapping_table)
insert_subject_character(conn, cursor, input_path, mapping_table)
insert_subject_relation(conn, cursor, input_path, mapping_table)
insert_person_character(conn, cursor, input_path)

conn.close()
