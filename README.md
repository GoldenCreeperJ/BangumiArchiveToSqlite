# Bangumi Archive to Sqlite

此工具用于将 Bangumi 归档数据转换为 Sqlite 数据库。

## 使用说明

### 转换流程
1. 从 `Archive` 和 `common` 仓库下载所需文件，并放入 `input` 目录中
2. 运行 `main.py` 开始转换，`output` 目录将生成一些有用的 json 文件  

### 文档说明
- `Summary.md` - 转换字段说明  
- `Converter.py` - 包含详细转换逻辑的注释  
- `MappingTable.json` - 自动生成的字段映射表  

### 数据迁移选项
| 迁移类型                   | 说明   | 基于               | 包含数据   |
|------------------------|------|------------------|--------|
| **StandardMigrator**   | 标准迁移 | /                | 完整原始数据 |
| **MiniMigrator**       | 精简迁移 | StandardMigrator | 移除社交数据 |
| **PersonalMigrator**   | 个人迁移 | MiniMigrator     | 增加个人数据 |
| **AnimeMigrator**      | 动漫迁移 | PersonalMigrator | 保留动漫数据 |
| **JapanAnimeMigrator** | 日漫迁移 | AnimeMigrator    | 筛选日漫数据 |

## 相关资源链接
- [BangumiArchiveExplain](https://github.com/Livinfly/BangumiArchiveExplain/tree/7310d74797977d3a8e8e4c9092b13158eb333cd9)
- [Archive](https://github.com/bangumi/Archive/tree/9a897d0df30f2c0afdeeaebae742493139af1a87) 
- [wiki-parser-py](https://github.com/bangumi/wiki-parser-py/tree/af736437d75546a89718498341f2eb3556e9a402)
- [common](https://github.com/bangumi/common/tree/6a8442c17143a870357a5ff812362e8b5cfe9f9d)
- [server](https://github.com/bangumi/server/tree/6d2170541b291ca7a1fd917602a38e3f6f2e0fda)
- [测试用数据快照](https://github.com/bangumi/Archive/releases/download/archive/dump-2026-07-07.210439Z.zip)