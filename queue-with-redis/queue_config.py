from rq import Queue
from redis import Redis
from config import REDIS_URL

redis_client = Redis.from_url(REDIS_URL)

email_queue = Queue("email", connection=redis_client)
