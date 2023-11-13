# conmmand line
https://www.odoo.com/documentation/12.0/developer/reference/cmdline.html#reference-cmdline

## run odoo with remote PG server
1. docker build -t odoo-db -f Dockerfile.12 . 
2. docker run -p 8069:8069 -e USER=dev -e PASSWORD=odooodoo -e HOST=139.196.213.108 -e PORT=9002  -it odoo-db # -e DB_NAME=odoo
3. local UI http://localhost:8069/web
4. create db: http://0.0.0.0:8069/web/database/manager

## odoo 16.0
1. docker run -v /path/to/addons:/mnt/extra-addons -v /path/to/config:/etc/odoo -p 8069:8069 --name odoo:16.0 -t odoo
2. ali ecs: docker run -it -v /root/odoo/addons:/mnt/extra-addons -v /root/odoo:/etc/odoo -v /root/odoo:/etc/odoo -v /root/_git/files/odoo-data:/var/lib/odoo -p 8069:8069  --restart=always odoo:16.0