import os

rabbit_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbit_pw = os.getenv("RABBITMQ_DEFAULT_PASS")
rabbit_url = os.getenv("RABBITMQ_URL")

broker_url = f"pyamqp://{rabbit_user}:{rabbit_pw}@{rabbit_url}//"
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = "Asia/Taipei"
enable_utc = True
