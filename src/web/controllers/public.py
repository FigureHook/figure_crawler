from flask import Blueprint, render_template

from web.forms import SubscriptionForm

blueprint = Blueprint("public", __name__)


@blueprint.route("/", methods=["GET"])
def home():
    """Home page"""
    form = SubscriptionForm(
        redirect_uri="http://127.0.0.1:8000/webhook"
    )
    return render_template("index.html", form=form)
