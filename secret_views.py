from flask import Blueprint
from flask import render_template
from flask_login import login_required

secret_blueprint = Blueprint(
    "secret",
    __name__,
    url_prefix="/secret",
    template_folder="templates",
)


@secret_blueprint.route("/")
@login_required
def message(methods=["GET"]):
    return render_template("secret.html")
