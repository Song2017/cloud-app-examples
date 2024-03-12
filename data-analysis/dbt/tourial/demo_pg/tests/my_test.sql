select count(*)
from {{ref("my_second_dbt_model")}}
where id = 2