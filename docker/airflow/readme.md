## Running Airflow
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml'
```shell
docker compose down --volumes --remove-orphans
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up
# docker compose up -d
```
access  http://localhost:8080/login/
airflow/airflow

## Running the CLI commands
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.3/airflow.sh'
chmod +x airflow.sh

./airflow.sh info/bash/python
```

## docker command
```shell
docker run -it -e _AIRFLOW_WWW_USER_PASSWORD=pass -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://user:ad***@120.46.78.85:30012/airflow -e AIRFLOW__CELERY__BROKER_URL=redis://re***:@120.46.78.85:31000/1 apache/airflow:2.7.3
```

## note
1. 从root切换到airfow， root下没有python： su airflow