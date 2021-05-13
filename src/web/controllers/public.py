import os
from base64 import b64encode
from os import urandom

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from web.forms import SubscriptionForm

blueprint = Blueprint("public", __name__)


def discord_redirect_url(state):
    base_uri = "https://discord.com/api/oauth2/authorize"
    redirect_uri = url_for('auth.webhook', _external=True)
    client_id = os.getenv('DISCORD_CLIENT_ID')
    return "{}?response_type=code&client_id={}&scope=webhook.incoming&redirect_uri={}&state={}".format(
        base_uri, client_id, redirect_uri, state
    )


@blueprint.route("/", methods=('GET', 'POST'))  # type: ignore
def home():
    """Home page"""
    form = SubscriptionForm()
    if request.method == 'GET':
        return render_template("index.html", form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            state = b64encode(urandom(12)).decode('utf-8')
            session['state'] = state
            location = discord_redirect_url(state)

            session['webhook_setting'] = {
                'is_nsfw': form.is_nsfw.data,
                'lang': form.language.data
            }

            return redirect(location)

        flash("wtf are you doing?")
        return render_template("index.html", form=form, error="WTF?")
