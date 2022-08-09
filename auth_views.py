from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import request
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from models import User

auth_blueprint = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="templates",
)


@auth_blueprint.route("/validate-login", methods=["POST"])
def validate_login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter(User.email == email).first()

    if user is None:
        return redirect("home")
    else:
        if user.check_password(password):
            login_user(user)
            return redirect(url_for("secret.message"))
        else:
            return redirect(url_for("home"))


@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("home"))
