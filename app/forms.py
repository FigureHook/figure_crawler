import os

from flask_wtf import FlaskForm
from wtforms import HiddenField


class SubscriptionForm(FlaskForm):
    response_type = HiddenField(default="code")
    client_id = HiddenField(default=os.getenv("DISCORD_CLIENT_ID"))
    scope = HiddenField(default="webhook.incoming")
    redirect_uri = HiddenField()
