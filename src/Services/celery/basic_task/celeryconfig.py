import os

rabbit_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbit_pw = os.getenv("RABBITMQ_DEFAULT_PASS")

broker_url = f"pyamqp://{rabbit_user}:{rabbit_pw}@rabbit:5672//"
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = "Asia/Taipei"
enable_utc = True
