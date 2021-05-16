import os
from base64 import urlsafe_b64encode
from os import urandom

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_babel import get_locale

from web.forms import SubscriptionForm, language_choices

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
    locale = get_locale()
    default_lang_choice = language_choices().get(str(locale))
    form.language.default = default_lang_choice[0]
    form.process()

    if request.method == 'GET':
        return render_template("index.html", form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            state = urlsafe_b64encode(urandom(12)).decode('utf-8')
            session['state'] = state
            location = discord_redirect_url(state)

            session['webhook_setting'] = {
                'is_nsfw': form.is_nsfw.data,
                'lang': form.language.data
            }

            return redirect(location)

        flash("wtf are you doing?")
        return render_template("index.html", form=form, error="WTF?")
