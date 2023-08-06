from flask import Blueprint, render_template, request, redirect, url_for
from .models import Users, Players, Characters, Roles, Role_Entries
from . import db

views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@views.route("/email", methods=["GET", "POST"])
def email():
    if request.method == "POST":
        email = request.form.get("email")
        print(email)
        user = Users.query.filter_by(email=email).first()
        if user:
            return redirect("/error")
        new_user = Users(email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("views.email"))
    return render_template("email.html")


@views.route("/player_entry", methods=["GET", "POST"])
def player_entry():
    if request.method == "POST":
        playerName = request.form.get("playerName")
        characterName = request.form.get("characterName")
        role = request.form.get("role")
        new_player = Players(PlayerName=playerName)
        db.session.add(new_player)
        new_character = Characters(CharacterName=characterName, PlayerName=playerName, Role=role)
        db.session.add(new_character)
        db.session.commit()
        
    return render_template("player_entry.html")



@views.route("/error", methods=["GET"])
def error():
    return render_template("error.html")