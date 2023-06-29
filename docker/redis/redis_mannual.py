import base64
import functools
import json
import os

import arrow
from cached_property import cached_property

from redis import Redis


def decorator(func):

    @functools.wraps(func)
    def wrapper(*arg, **kwargs):
        print("begin..", str(func), arrow.now())
        result = func(*arg, **kwargs)
        print("end..", arrow.now())
        return result

    return wrapper


class RawDataEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, bytes):
            return o.decode("utf-8")
        return super(RawDataEncoder, self).default(o)


class FreightDB:

    @cached_property
    def freight_redis(self) -> Redis:
        """
        freight redis client
        """

        # noqa:E501
        password = os.getenv("REDIS_SERVER_PASSWORD", "PS4")
        if not password:
            raise Exception("no redis settings.")
        return Redis(
            host=os.getenv("REDIS_SERVER_HOST1",
                           "redis.rds.aliyuncs.com"),
            port=6379,
            decode_responses=True,
            password=password,
            socket_timeout=10,
        )

    def b64encode(self, content: str) -> str:
        type(self)
        return base64.b64encode(content.encode("utf-8")).decode("utf-8")

    def json_dumps_unicode(self, obj):
        """
        Change Python default json.dumps acting like JavaScript, including allow
        Chinese characters and no space between any keys or values.
        """  # noqa:E501
        type(self)
        return json.dumps(obj,
                          ensure_ascii=False,
                          separators=(',', ':'),
                          cls=RawDataEncoder)


@decorator
def backup_table(redis_db: FreightDB, table_name: str):
    redis_cli = redis_db.freight_redis

    ori_data = str(redis_cli.hgetall(table_name))
    import pdb
    pdb.set_trace()
    ori_data = ori_data.replace("'", '"')
    data = json.loads(ori_data)
    records = redis_cli.hset(
        table_name + "_test", mapping=data
    )
    print("carrier-store updated record", records)


if __name__ == '__main__':
    print("begin----")
    redis_db = FreightDB()
    backup_table(redis_db, "ENVOY_YOUZAN_CYPHER_STORE_SHOP")
