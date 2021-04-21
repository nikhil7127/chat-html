from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .templates.codes.mail import sendEmail

views = Blueprint("views", __name__)


@views.route("/mail", methods=["POST", "GET"])
@login_required
def mail():
    if request.method == "POST":
        data = request.form
        senderEmail, senderPassword = data.get("senderEmail"), data.get("senderPassword")
        recvEmail = data.get("recvEmail")
        subject, body = data.get("subject"), data.get("body")
        status = sendEmail((senderEmail, senderPassword), recvEmail, {"subject": subject, "body": body})
        if status == "loginError":
            flash("Error while logging you make sure that you allow less secure apps option on", "error")
        elif status == "messageSuccess":
            flash("email send successfully", "success")
        elif status == "messageError":
            flash("Error while sending message", "error")
        return redirect(url_for("views.home"))
    return render_template("mail.html", currentUser=current_user)


@views.route("/")
@login_required
def home():
    return render_template("home.html", currentUser=current_user)
