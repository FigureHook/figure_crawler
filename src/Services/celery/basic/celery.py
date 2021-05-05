from celery import Celery

app = Celery("celery", include=("basic.tasks"))
app.config_from_object("basic.celeryconfig")


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(minute="*/10"),
#         news_push.s(),
#         name="push new release through discord webhook",
#     )
#     sender.add_periodic_task(
#         crontab(minute="*/30"),
#         check_new_release.s(),
#         name="check product every half-hour",
#     )
