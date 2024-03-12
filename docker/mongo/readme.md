# Mongo & Mongo express powered by compose
https://hub.docker.com/_/mongo
```
docker-compose up

-- --network some-network 
docker run -d --name mongo -p 27017:27017 \
	-e MONGO_INITDB_ROOT_USERNAME=root \
	-e MONGO_INITDB_ROOT_PASSWORD=pass \
	mongo
```
mongo compass connection: `mongodb://root:pass@localhost:27017/`

# Restore the MongoDB physical backup file to the local database
阿里云下载的物理备份文件是xbstream格式(_qp.xb), 使用前要先解压。

1. percona-xtrabackup解压：
- xtrabackup 8.0之后，解压改为xtrabackup。     
- 阿里云数据库MongoDB默认使用的是WiredTiger存储引擎，并且开启了directoryPerDB选项。
解压后的文件夹里每个DB都有一个文件夹
```
mv _qp.xb /Users/songgs/Desktop/cache/data
docker run --name percona -v /Users/songgs/Desktop/cache:/backup-directory -it percona/percona-xtrabackup sh
cd /backup-directory/data
cat _qp.xb | xbstream -x -v
xtrabackup --decompress --remove-original --target-dir=/backup-directory/data
```
2. 恢复到本地Mongo Server
- mongo.conf
```
systemLog:
    destination: file
    path: /test/mongo/mongod.log
    logAppend: true
security:
    authorization: enabled
storage:
    dbPath: /data/db
    directoryPerDB: true
processManagement:
    fork: true
    pidFilePath: /test/mongo/mongod.pid
```
- docker service
`docker run -it -p 27015:27017 -v /Users/songgs/Desktop/cache/data:/data/db -v /Users/songgs/Desktop/cache/mongod.conf:/etc/mongod.conf mongo:4.2.24`
- connection string
`mongodb://localhost:27015/`
3. 同步本地数据到阿里云
用Python脚本从本地数据库取数据，然后写到线上数据库
```
import os

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

mongo_url = os.getenv('MONGO_URL')
client = MongoClient(mongo_url)
local_client: MongoClient = MongoClient("mongodb://localhost:27015")

db_name = "storefront-account-service"
store_database = client[db_name]
local_client.list_databases()
ol_db = client[db_name]
local_store_db: Database = local_client[db_name]

for coll_name in local_store_db.list_collection_names():
    coll: Collection = local_store_db[coll_name]
    print(coll_name)
    for i in coll.find().sort("_id"):
        ol_db[coll_name].update_one(
            {"_id": i["_id"]},
            {'$set': i},
            upsert=True)
```

# 参考
- https://www.alibabacloud.com/help/zh/mongodb/user-guide/restore-data-of-an-apsaradb-for-mongodb-instance-to-a-self-managed-mongodb-database-by-using-physical-backups