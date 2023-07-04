# Transfer Redis data between different RDB format version
# fix: Can't handle RDB format version 11

from redis import Redis


class Cache:
    source: Redis = None
    target: Redis = None
    keys: dict = {}

    _types = ("hash", "string", "list", "set", "zset", "stream")

    def get_keys(self) -> dict:
        self.keys = {i: [] for i in self._types}
        for _type in self._types:
            cursor = '0'
            while cursor != 0:
                cursor, data = self.source.scan(
                    cursor, match=None, _type=_type)
                self.keys[_type].extend(data)
        return self.keys

    def transfer(self, _types: list = None, _keys: dict = None):
        # todo zset, stream
        assert _keys or self.keys, "get keys from source db first"
        _types = _types or self._types
        self.keys = _keys or self.keys

        for _type in _types:
            print(_type, getattr(self, f"transfer_{_type}")())

    def transfer_hash(self) -> bool:
        for key in self.keys["hash"]:
            data = self.source.hgetall(key)
            self.target.hset(key, mapping=data)
        return True

    def transfer_string(self) -> bool:
        for key in self.keys["string"]:
            data = self.source.get(key)
            self.target.set(key, data)
        return True

    def transfer_list(self) -> bool:
        for key in self.keys["list"]:
            data = self.source.lrange(key, 0, -1)
            self.target.rpush(key, *data)
        return True

    def transfer_set(self) -> bool:
        for key in self.keys["set"]:
            data = self.source.smembers(key)
            self.target.sadd(key, *data)
        return True

    @staticmethod
    def redis_cli(host: str, password: str, port=6379, db=0) -> Redis:
        assert password
        return Redis(
            db=int(db), host=host, port=int(port),
            password=password,
            decode_responses=True,
            socket_timeout=5,
        )


if __name__ == '__main__':
    _db = 0
    source_pass = ["333.196.213.108", "Pass123", "6379", _db]
    target_pass = ["222.46.78.85", "Pass123", "31779", _db]
    c = Cache()
    c.source = Cache.redis_cli(*source_pass)
    print(c.get_keys())
    c.target = Cache.redis_cli(*target_pass)
    c.transfer(_types=["hash", "string", "list", "set"])
