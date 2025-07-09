import json
import yaml
from util.Parser import Wiki


def yaml_to_json():
    """
        将YAML文件转换为JSON文件
        部分缺失信息需手动补充
    """
    with open("./input/subject_platforms.yml", 'r', encoding='utf-8') as f:
        platforms = yaml.safe_load(f)
    with open("./input/subject_relations.yml", 'r', encoding='utf-8') as f:
        relations = yaml.safe_load(f)
    with open("./input/subject_staffs.yml", 'r', encoding='utf-8') as f:
        staffs = yaml.safe_load(f)
    result = {
        "rating": {0: "未知", 1: "烂作", 2: "庸作", 3: "佳作", 4: "神作"},  # Subject rating
        "status": {0:  "未看", 1: "想看", 2: "在看", 3: "已看", 4: "弃看"},  # Subject status
        "book_series": {0: "单行本", 1: "系列", 2: ""},  # Subject series
        "subject_types": {1: "漫画", 2: "动画", 3: "音乐", 4: "游戏", 6: "三次元"},  # Subject type
        "person_types": {0: "未知", 1: "个人", 2: "公司", 3: "组合"},  # Person type
        "character_role": {1: "角色", 2: "机体", 3: "舰船", 4: "组织机构"},  # Character role
        "episode_types": {0: "正篇", 1: "特别篇", 2: "OP", 3: "ED", 4: "Trailer", 5: "MAD", 6: "其他"},  # Episode type
        "character_types": {1: "主角", 2: "配角", 3: "客串", 4: "闲角", 5: "旁白", 6: "声库"},  # Subject-Character type
        "subject_platforms": {i: {j: k['type_cn'] for j, k in platforms['platforms'][i].items()} for i in (1, 2, 4, 6)},  # Subject platform
        "subject_relations": {j: k['cn'] for i in relations['relations'].values() for j, k in i.items()},  # Subject-Relation relation-type
        "subject_staffs": {j: k['cn'] for i in staffs['staffs'].values() for j, k in i.items()}}  # Subject-Person position
    result["subject_platforms"][3] = {0: "其他"}
    result["subject_relations"][4013] = "其他"

    tasks = [
        ("subject", [
            lambda item: result["subject_types"][item['type']],
            lambda item: result["subject_platforms"][item['type']][item['platform']],
            lambda item: result["book_series"][1 if item["series"] else 0]
        ]),
        ("character", [
            lambda item: result["character_role"][item['role']]
        ]),
        ("person", [
            lambda item: result["person_types"][item['type']]
        ]),
        ("episode", [
            lambda item: result["episode_types"][item['type']]
        ]),
        ("subject-characters", [
            lambda item: result["character_types"][item["type"]]
        ]),
        ("subject-persons", [
            lambda item: result["subject_staffs"][item["position"]]
        ]),
        ("subject-relations", [
            lambda item: result["subject_relations"][item["relation_type"]]
        ]),
    ]

    for filename, handlers in tasks:
        with open(f"./input/{filename}.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())
                for handler in handlers:
                    try:
                        handler(item)
                    except Exception as e:
                        print(f'{filename} 映射失败：{e}')

    with open("./util/MappingTable.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print("\n映射表创建完成\n")


def jsonl_to_json():
    """
        将JSONL文件转换为JSON文件
        以便使用JSON的表格视图功能
    """
    for filename in ["subject", "character", "person", "episode", "subject-characters",
                     "subject-persons", "subject-relations", "person-characters"]:
        json_array = []

        with open(f"./input/{filename}.jsonlines", 'r', encoding='utf-8') as f:
            for line in f:
                json_object = json.loads(line.strip())
                json_array.append(json_object)

        with open(f"./output/{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(json_array, f, ensure_ascii=False, indent=4)

        print(f"已转换 {filename}")

    print("\nJSON文件转换完成\n")


def infoBox_to_json(s: str) -> str:
    try:
        return json.dumps(dict(Wiki(s)), ensure_ascii=False, indent=4)
    except Exception as e:
        print(e, s)
        return ""
