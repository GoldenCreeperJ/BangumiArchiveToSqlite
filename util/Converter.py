import json
import yaml
from util.Parser import Wiki


def jsonl_to_json(input_file, output_file):
    """
    Convert a JSONL file to a JSON file.
    In order to use the json's table view
    """
    json_array = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            json_object = json.loads(line.strip())
            json_array.append(json_object)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_array, f, ensure_ascii=False, indent=4)

    print(f"Converted {input_file} to {output_file}")


def yaml_to_json(input_path, output_file):
    """
    Convert a YAML file to a JSON file.
    Some lack information is added manually.
    """
    with open(input_path + "/subject_platforms.yml", 'r', encoding='utf-8') as f:
        platforms = yaml.safe_load(f)
    with open(input_path + "/subject_relations.yml", 'r', encoding='utf-8') as f:
        relations = yaml.safe_load(f)
    with open(input_path + "/subject_staffs.yml", 'r', encoding='utf-8') as f:
        staffs = yaml.safe_load(f)
    result = {
        "rating": {0: "未知", 1: "烂作", 2: "庸作", 3: "佳作", 4: "神作"},  # Subject rating
        "status": {0:  "未看", 1: "想看", 2: "在看", 3: "已看", 4: "弃看"},  # Subject status
        "book_series": {0: "单行本", 1: "系列", 2: ""},  # Subject series
        "subject_types": {1: "漫画", 2: "动画", 3: "音乐", 4: "游戏", 6: "三次元"},  # Subject type
        "person_types": {0: "未知", 1: "个人", 2: "公司", 3: "组合"},  # Person type
        "character_role": {1: "角色", 2: "机体", 3: "组织", 4: "标志"},  # Character role
        "episode_types": {0: "正篇", 1: "特别篇", 2: "OP", 3: "ED", 4: "Trailer", 5: "MAD", 6: "其他"},  # Episode type
        "character_types": {1: "主角", 2: "配角", 3: "客串"},  # Subject-Character type
        "subject_platforms": {i: {j: k['type_cn'] for j, k in platforms['platforms'][i].items()} for i in (1, 2, 4, 6)},  # Subject platform
        "subject_relations": {j: k['cn'] for i in relations['relations'].values() for j, k in i.items()},  # Subject-Relation relation-type
        "subject_staffs": {j: k['cn'] for i in staffs['staffs'].values() for j, k in i.items()}}  # Subject-Person position
    result["subject_platforms"][3] = {0: "其他"}
    result["subject_relations"][4018] = "未知"
    result["subject_relations"][4019] = "未知"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"Converted {input_path} to {output_file}")


def infoBox_to_json(s: str) -> str:
    try:
        return json.dumps(dict(Wiki(s)), ensure_ascii=False, indent=4)
    except Exception as e:
        print(e, s)
        return ""
