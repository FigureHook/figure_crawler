from flask import Blueprint, request
from flask.helpers import url_for
from werkzeug.utils import redirect

blueprint = Blueprint("auth", __name__)


@blueprint.route("/webhook", methods=["GET"])
def webhook():
    # TODO: exchange for access token
    print(request.args.to_dict())
    return redirect(url_for("public.home"))
