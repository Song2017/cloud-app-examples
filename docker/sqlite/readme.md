1. docker
```
docker run -d --name=sqlitebrowser     -e PUID=1000  -e PGID=1000  -e TZ=Etc/UTC  -p 3000:3000 --restart unless-stopped lscr.io/linuxserver/sqlitebrowser:latest
  <!-- 
  --security-opt seccomp=unconfined `#optional`
  -p 3001:3001 \
  -v /path/to/config:/config \
  -e FILE__MYVAR=/run/secrets/mysecretvariable
  --restart unless-stopped \
  lscr.io/linuxserver/sqlitebrowser:latest
   -->
```
2. mac
```
https://www.runoob.com/sqlite/sqlite-create-database.html
brew install sqlite

sqlite3
.open test.db
```


