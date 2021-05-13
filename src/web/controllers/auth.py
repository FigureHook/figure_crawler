import os

import requests as rq
from flask import Blueprint, flash, request
from flask.helpers import url_for
from werkzeug.utils import redirect

from Models import Webhook

blueprint = Blueprint("auth", __name__)

API_ENDPOINT = "https://discord.com/api/v8"


def exchange_token(code):
    data = {
        "client_id": os.getenv("DISCORD_CLIENT_ID"),
        "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": url_for("public.home", _external=True)
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = rq.post(f"{API_ENDPOINT}/oauth2/token", data=data, headers=headers)
    return r


def save_webhook_info(channel_id, _id, token):
    the_hook = Webhook.get_by_channel_id(channel_id)
    if the_hook:
        the_hook.update(id=_id, token=token)
    if not the_hook:
        the_hook = Webhook.create(channel_id=channel_id, id=_id, token=token)
    the_hook.session.commit()


@blueprint.route("/webhook", methods=["GET"])
def webhook():
    args = request.args.to_dict()

    r = exchange_token(args["code"])

    if r.status_code == 200:
        webhook_response = r.json()
        webhook_channel_id = webhook_response["webhook"]["channel_id"]
        webhook_id = webhook_response["webhook"]["id"]
        webhook_token = webhook_response["webhook"]["token"]
        save_webhook_info(webhook_channel_id, webhook_id, webhook_token)
        flash("Hooking success!")
    else:
        flash("Webhook authorization failed.")

    return redirect(url_for("public.home"))
