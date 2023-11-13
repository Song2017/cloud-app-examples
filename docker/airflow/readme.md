https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml'
```shell
docker compose down --volumes --remove-orphans
docker compose up airflow-init
docker compose up
```
access  http://localhost:8080/login/
airflow/airflow
