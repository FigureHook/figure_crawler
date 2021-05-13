import os

from flask import Blueprint, flash, redirect, render_template, request, url_for

from web.forms import SubscriptionForm

blueprint = Blueprint("public", __name__)


def discord_redirect_url():
    base_uri = "https://discord.com/api/oauth2/authorize"
    redirect_uri = url_for('auth.webhook', _external=True)
    client_id = os.getenv('DISCORD_CLIENT_ID')
    return f"{base_uri}?response_type=code&client_id={client_id}&scope=webhook.incoming&redirect_uri={redirect_uri}"


@blueprint.route("/", methods=('GET', 'POST'))  # type: ignore
def home():
    """Home page"""
    form = SubscriptionForm()
    if request.method == 'GET':
        return render_template("index.html", form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            location = discord_redirect_url()
            return redirect(location)

        flash("wtf are you doing?")
        return render_template("index.html", form=form, error="WTF?")
