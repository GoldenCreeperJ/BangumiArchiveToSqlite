# Bangumi Archive to Sqlite

This is a tool to convert the Bangumi Archive to Sqlite database.

## Usage
Download necessary files from `Archive` and `common` repository, and put them in the `input` directory.  
Run the `main.py` to start the conversion,some useful json files will be generated in the `output` directory.  
Read `Summary.md`, comments in `Converter.py`  and generated `MappingTable.json` for more transformation details.  
`StandardMigrator` is used to migrate the data to sqlite database without any changes.  
`MiniMigrator` is based on the `StandardMigrator` and drops some social data like comments, collects, rank, score, etc.  
`PersonalMigrator` is based on the `MiniMigrator` and adds some personal data like status, rating, etc.  

### References:
- [BangumiArchiveExplain](https://github.com/Livinfly/BangumiArchiveExplain/tree/7310d74797977d3a8e8e4c9092b13158eb333cd9)
- [Archive](https://github.com/bangumi/Archive/tree/53d1e103e81c34e39343b641b771459ff8e32aad) 
- [wiki-parser-py](https://github.com/bangumi/wiki-parser-py/tree/d36c8459eef2211878ea72f991190f566f536216)
- [common](https://github.com/bangumi/common/tree/510d5fbf0cc49eb843e2d6583c00345a75a083e1)
- [server](https://github.com/bangumi/server/tree/edd75802f4fb713213aa30f2e3854e3c019737b9)
- [dump](https://github.com/bangumi/Archive/releases/download/archive/dump-2025-06-17.210250Z.zip)