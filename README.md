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
- [Archive](https://github.com/bangumi/Archive/tree/114cb0ff036145b7458e7136abd32f0cdaf7e52b) 
- [wiki-parser-py](https://github.com/bangumi/wiki-parser-py/tree/d1f1eb7b0dda8e8ce25c34a17300e427c9bd241b)
- [common](https://github.com/bangumi/common/tree/85904677af13a7b70789c5892369ae49e8ae6f47)
- [server](https://github.com/bangumi/server/tree/3ef2cf0d557d71fa2e9957cf703aec6c7607f340)
- [测试用数据快照](https://github.com/bangumi/Archive/releases/download/archive/dump-2025-07-08.210304Z.zip)