#!/bin/sh
# docker run -dt --restart=always -p 8080:8080 songgs/jd
# https://www.nginx.com/resources/wiki/start/topics/examples/full/
set -e
echo '''
error_log  logs/error.log;

server {
    listen       8080;
    listen  [::]:8080;
    server_name  localhost;

    log_format   main '$remote_addr - $remote_user [$time_local]  $status '
        '"$request" $body_bytes_sent "$http_referer" '
        '"$http_user_agent" "$http_x_forwarded_for"';
    access_log   logs/access.log  main;

    location /index {
        root   /usr/share/nginx/html;
    }

    location / {
      client_max_body_size 0;
      gzip off;

      proxy_cache off;

      proxy_read_timeout      300;
      proxy_connect_timeout   300;
      proxy_redirect          off;

      proxy_http_version 1.1;

      #proxy_set_header    Host                $http_host;
      #proxy_set_header    X-Real-IP           $remote_addr;
      proxy_set_header    X-Forwarded-Ssl     on;
      proxy_set_header    X-Forwarded-For     $proxy_add_x_forwarded_for;
      proxy_set_header    X-Forwarded-Proto   $scheme;
      proxy_pass https://openapi-fxg.jinritemai.com;
    }

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}
} ''' >> /etc/nginx/conf.d/app.conf

exec "$@"