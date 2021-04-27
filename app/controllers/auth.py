import os

import requests as rq
from flask import Blueprint, request
from flask.helpers import url_for
from werkzeug.utils import redirect

from src.Models import Webhook

blueprint = Blueprint("auth", __name__)
API_ENDPOINT = "https://discord.com/api/v8"


@blueprint.route("/webhook", methods=["GET"])
def webhook():
    args = request.args.to_dict()
    data = {
        "client_id": os.getenv("DISCORD_CLIENT_ID"),
        "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": args["code"],
        "redirect_uri": "http://127.0.0.1:8000/webhook"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = rq.post(f"{API_ENDPOINT}/oauth2/token", data=data, headers=headers)

    if r.status_code == 200:
        webhook_response = r.json()
        webhook_channel_id = webhook_response["webhook"]["channel_id"]
        webhook_url = webhook_response["webhook"]["url"]
        the_hook = Webhook.get_by_channel_id(webhook_channel_id)
        if the_hook:
            the_hook.update(url=webhook_url)
        if not the_hook:
            the_hook = Webhook.create(channel_id=webhook_channel_id, url=webhook_url)
        the_hook.session.commit()

    return redirect(url_for("public.home"))
