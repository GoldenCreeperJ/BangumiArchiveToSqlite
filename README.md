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
- [Archive](https://github.com/bangumi/Archive/tree/78d0bc791fc47f4385a708ed8c8a29d748301611) 
- [wiki-parser-py](https://github.com/bangumi/wiki-parser-py/tree/e5fdb584573265359ecae5fcad6dd279ffbfd59e)
- [common](https://github.com/bangumi/common/tree/6a8442c17143a870357a5ff812362e8b5cfe9f9d)
- [server](https://github.com/bangumi/server/tree/4a555f9ee07c794062b3b38387db6023cc5e6ca4)
- [测试用数据快照](https://github.com/bangumi/Archive/releases/download/archive/dump-2026-01-20.210310Z.zip)