from rq import Worker
from queue_config import email_queue, redis_client

email_worker = Worker([email_queue], name="email", connection=redis_client)

if __name__ == "__main__":
    email_worker.work()