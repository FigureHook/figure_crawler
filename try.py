from figure_hook.database import pgsql_session
from figure_hook.Models import Webhook
from figure_hook.Tasks.on_demand import send_discord_welcome_webhook

with pgsql_session() as session:
    ws = session.query(Webhook).where(Webhook.channel_id == "855366227329417256").first()
    assert type(ws) is Webhook
    print(ws.lang)

    send_discord_welcome_webhook(ws.id, ws.decrypted_token, "test message")