FROM nginx:1.23-alpine-slim
LABEL maintainer="Dev <Dev1@samarkand.global>"

COPY docker-entrypoint.sh /app/docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]