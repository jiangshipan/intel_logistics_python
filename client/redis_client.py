import redis
from config import config
pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT)
redis_client = redis.Redis(connection_pool=pool)