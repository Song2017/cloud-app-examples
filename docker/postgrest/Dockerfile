FROM registry.cn-shanghai.aliyuncs.com/public_00/postgrest:v12.2.3

# Copy the configuration file into the container
COPY postgrest.conf /etc/postgrest.conf

# Set the command to run PostgREST
CMD ["postgrest", "/etc/postgrest.conf"]