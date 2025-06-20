##### **Subject(作品)**

|              |                                  |                      |
|--------------|----------------------------------|----------------------|
| ID           | number                           |                      |
| Type         | number*                          | 类型                   |
| Name         | string                           | 名字                   |
| NameCN       | string                           | 简体中文名                |
| Infobox      | string                           |                      |
| Platform     | number*                          | 媒介（类别）               |
| Summary      | string                           | 简介                   |
| Nsfw         | bool                             | not safe for work    |
| Tags         | [{string:string, string:number}] | 公共标签                 |
| meta_tags    | string                           | 公共标签                 |
| Score        | number                           | 评分                   |
| ScoreDetails | [{string:number}]                | 评分细节                 |
| Rank         | number                           | 类别内排名                |
| Date         | string                           | 发行日期                 |
| Favorite     | [{string:number}]                | 收藏状态（想看、看过、在看、搁置、抛弃） |
| Series       | bool*                            | 系列（单行本？）             |

##### **Person(人物)**

|          |          |              |
|----------|----------|--------------|
| ID       | number   |              |
| Name     | string   | 名字           |
| Type     | number*  | 分类           |
| Career   | [string] | 职业           |
| Infobox  | string   |              |
| Summary  | string   | 简介           |
| Comments | number   | 评论/吐槽数（含楼中楼） |
| Collects | number   | 收藏数          |

##### **Character(角色)**

|          |         |              |
|----------|---------|--------------|
| ID       | number  |              |
| Role     | number* | 角色类型         |
| Name     | string  | 姓名           |
| Infobox  | string  |              |
| Summary  | string  | 简介           |
| Comments | number  | 评论/吐槽数（含楼中楼） |
| Collects | number  | 收藏数          |

##### **Episode(剧集)**

|             |         |                      |
|-------------|---------|----------------------|
| ID          | number  |                      |
| Name        | string  | 名字                   |
| NameCn      | string  | 简体中文名                |
| Description | string  | 描述（常包含staff，summary） |
| AirDate     | string  | 首播日期                 |
| Disc        | number  | 第[disc]张光盘           |
| Duration    | string  | 时长                   |
| SubjectID   | number  |                      |
| Sort        | number  | 序话，第[sort]集          |
| Type        | number* | 类型                   |

##### **SubjectRelation(作品-作品)**

|                  |         |      |
|------------------|---------|------|
| SubjectID        | number  |      |
| RelationType     | number* | 关联类型 |
| RelatedSubjectID | number  |      |
| Order            | number  | 关联排序 |

##### **SubjectCharacter(作品-角色)**

|             |         |                                    |
|-------------|---------|------------------------------------|
| CharacterID | number  |                                    |
| SubjectID   | number  |                                    |
| Type        | number* | 类型                                 |
| Order       | number  | 作品角色列表排序（按type和order排序，order不保证连续） |

##### **SubjectPerson(作品-人物)**

|           |         |      |
|-----------|---------|------|
| PersonID  | number  |      |
| SubjectID | number  |      |
| Position  | number* | 担任职位 |

##### **PersonCharacter(人物-角色)**

|             |        |       |
|-------------|--------|-------|
| PersonID    | number |       |
| SubjectID   | number |       |
| CharacterID | number |       |
| Summary     | string | 概要（空） |