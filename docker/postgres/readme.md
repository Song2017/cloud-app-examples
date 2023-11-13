# Postgresql & PgAdmin powered by compose
ref: https://github.com/khezen/compose-postgres

## !! Warning
PgAdmin need to input Host inet address: 10.66.*.*
`inet 10.66.*.* netmask 0xfffff800 broadcast 10.66.111.255`

## Requirements:
* docker >= 17.12.0+
* docker-compose

## Quick Start
* Clone or download this repository
* Go inside of directory,  `cd compose-postgres`
* Run this command `docker-compose up -d`


## Environments
This Compose file contains the following environment variables:

* `POSTGRES_USER` the default value is **postgres**
* `POSTGRES_PASSWORD` the default value is **changeme**
* `PGADMIN_PORT` the default value is **5050**
* `PGADMIN_DEFAULT_EMAIL` the default value is **pgadmin4@pgadmin.org**
* `PGADMIN_DEFAULT_PASSWORD` the default value is **admin**

## Access to postgres: 
* `localhost:5432`
* **Username:** postgres (as a default)
* **Password:** changeme (as a default)

## Access to PgAdmin: 
* **URL:** `http://localhost:5050`
* **Username:** pgadmin4@pgadmin.org (as a default)
* **Password:** admin (as a default)

## Add a new server in PgAdmin:
* **Host name/address** `postgres`
* **Port** `5432`
* **Username** as `POSTGRES_USER`, by default: `postgres`
* **Password** as `POSTGRES_PASSWORD`, by default `changeme`

## Logging

There are no easy way to configure pgadmin log verbosity and it can be overwhelming at times. It is possible to disable pgadmin logging on the container level.

Add the following to `pgadmin` service in the `docker-compose.yml`:

```
logging:
  driver: "none"
```

[reference](https://github.com/khezen/compose-postgres/pull/23/files)


## local 
```
     docker run -itd --restart always -p 9002:5432 --volume pgvolume:/var/lib/postgresql -e POSTGRES_PASSWORD=admin123 -e POSTGRES_USER=user -e POSTGRES_DB=app -e POSTGRES_HOST_AUTH_METHOD=trust postgres:13.0-alpine

     docker run -itd --restart always -p 9002:9002 -e POSTGRES_PASSWORD=admin123 -e POSTGRES_USER=user -e POSTGRES_DB=app -e POSTGRES_HOST_AUTH_METHOD=trust postgres:15     
```